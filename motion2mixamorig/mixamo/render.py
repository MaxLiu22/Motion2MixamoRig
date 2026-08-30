"""Rendering for the Y Bot rig and mesh, with cameras taken from the calibration.

The anatomical FRONT / BACK / LEFT / RIGHT cameras are built from the validated
Y Bot Right / Up / Forward axes using the same construction that produced the
accepted orientation-check images. There is no image flip and no "camera on −Z"
rule compensating for a mapping error.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .kinematics import normalize

BG_BGR = (18, 18, 20)
GRID_BGR = (58, 56, 52)
SHADOW_BGR = (8, 8, 9)


@dataclass(frozen=True)
class Theme:
    """Panel palette. The floor runs far -> near so it reads as receding."""

    bg: tuple[int, int, int]
    floor_far: tuple[int, int, int]
    floor_near: tuple[int, int, int]
    grid: tuple[int, int, int]
    shadow: tuple[int, int, int]
    shadow_alpha: float
    # White joint dots vanish on a pale floor and leave the limbs looking dashed.
    joint: tuple[int, int, int]


# Black backdrop with the floor only just lifted off it, so the grid still reads
# as a surface while everything but the dancer stays out of the way.
DARK_THEME = Theme((0, 0, 0), (10, 10, 11), (22, 22, 25), (52, 51, 48), (0, 0, 0), 0.75,
                   (242, 242, 242))
# Sampled off the Mixamo viewport: flat 160 backdrop, floor 193 at the far edge
# rising to 204 underfoot, grid lines a little darker than the floor.
LIGHT_THEME = Theme((160, 160, 160), (193, 193, 193), (208, 208, 208), (168, 168, 168),
                    (108, 108, 108), 0.42, (48, 48, 48))
# For the character grid. Same mood as DARK_THEME but off black, because a
# navy or black outfit against a black backdrop has no silhouette to read.
GRID_THEME = Theme((30, 29, 27), (44, 43, 41), (66, 65, 62), (94, 92, 88), (0, 0, 0), 0.50,
                   (242, 242, 242))
PANEL_BAR_BGR = (16, 16, 18)
TEXT_BGR = (240, 240, 240)
MUTED_BGR = (136, 136, 136)
FLAG_BGR = (60, 60, 220)
LEFT_BGR = (232, 155, 76)
RIGHT_BGR = (90, 90, 224)
TORSO_BGR = (76, 200, 230)

MESH_COLORS_BGR = {
    "Alpha_Surface": np.array([200, 188, 180], dtype=np.float64),
    "Alpha_Joints": np.array([112, 104, 98], dtype=np.float64),
}

# The teal the Mixamo viewport gives the Y Bot, sampled off a screenshot.
MESH_COLORS_MIXAMO_BGR = {
    "Alpha_Surface": np.array([205, 180, 140], dtype=np.float64),
    "Alpha_Joints": np.array([120, 104, 84], dtype=np.float64),
}

# White shell over the stock grey joints. The white stops just under 255 on
# purpose: at 255 the lit faces clip and lose their shading.
MESH_COLORS_WHITE_BGR = {
    "Alpha_Surface": np.array([246, 246, 248], dtype=np.float64),
    "Alpha_Joints": np.array([112, 104, 98], dtype=np.float64),
}

VIEWS = ("front", "back", "left", "right")


@dataclass(frozen=True)
class Camera:
    """Orthographic anatomical view derived from the calibrated rig axes."""

    view: str
    look: np.ndarray
    cam_right: np.ndarray
    cam_up: np.ndarray
    center: np.ndarray
    scale: float
    width: int
    height: int

    def project(self, pts: np.ndarray) -> np.ndarray:
        d = np.asarray(pts, dtype=np.float64).reshape(-1, 3) - self.center
        u = d @ self.cam_right
        v = d @ self.cam_up
        x = self.width * 0.5 + u * self.scale
        y = self.height * 0.5 - v * self.scale
        return np.column_stack([x, y])

    def depth(self, pts: np.ndarray) -> np.ndarray:
        d = np.asarray(pts, dtype=np.float64).reshape(-1, 3) - self.center
        return d @ self.look

    def clip_near(self, poly: np.ndarray) -> np.ndarray:
        """Nothing is behind an orthographic camera, so this is the identity."""
        return np.asarray(poly, dtype=np.float64).reshape(-1, 3)

    def clip_segment(self, a: np.ndarray, b: np.ndarray):
        return a, b


@dataclass(frozen=True)
class PerspectiveCamera:
    """Pinhole view. Same project / depth / clip_near surface as Camera.

    An orthographic camera cannot show a floor receding to a vanishing point;
    every horizontal line stays parallel and evenly spaced. This one can.
    """

    eye: np.ndarray
    look: np.ndarray
    cam_right: np.ndarray
    cam_up: np.ndarray
    focal: float
    width: int
    height: int
    near: float = 0.05

    def project(self, pts: np.ndarray) -> np.ndarray:
        d = np.asarray(pts, dtype=np.float64).reshape(-1, 3) - self.eye
        z = np.maximum(d @ self.look, self.near)
        u = (d @ self.cam_right) / z * self.focal
        v = (d @ self.cam_up) / z * self.focal
        return np.column_stack([self.width * 0.5 + u, self.height * 0.5 - v])

    def depth(self, pts: np.ndarray) -> np.ndarray:
        d = np.asarray(pts, dtype=np.float64).reshape(-1, 3) - self.eye
        return d @ self.look

    def clip_near(self, poly: np.ndarray) -> np.ndarray:
        """Sutherland-Hodgman against z = near, so nothing behind the eye wraps."""
        p = np.asarray(poly, dtype=np.float64).reshape(-1, 3)
        z = self.depth(p) - self.near
        out = []
        for i in range(len(p)):
            j = (i + 1) % len(p)
            if z[i] >= 0.0:
                out.append(p[i])
            if (z[i] >= 0.0) != (z[j] >= 0.0):
                out.append(p[i] + z[i] / (z[i] - z[j]) * (p[j] - p[i]))
        return np.asarray(out, dtype=np.float64).reshape(-1, 3)

    def clip_segment(self, a: np.ndarray, b: np.ndarray):
        """Trim a world segment to the half-space in front of the eye, or drop it."""
        za, zb = (float(v) for v in self.depth(np.stack([a, b])) - self.near)
        if za < 0.0 and zb < 0.0:
            return None
        if za < 0.0:
            a = a + za / (za - zb) * (b - a)
        elif zb < 0.0:
            b = b + zb / (zb - za) * (a - b)
        return a, b

    @property
    def fov_deg(self) -> float:
        return float(2.0 * np.degrees(np.arctan(self.height * 0.5 / self.focal)))


def view_basis(axes: dict, view: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Same anatomical camera construction as the accepted orientation check.

    FRONT: stand on +Forward and look at the face/chest.
    BACK:  stand on −Forward. LEFT / RIGHT: stand on that anatomical side.
    """
    right = np.asarray(axes["right"], dtype=np.float64)
    up = np.asarray(axes["up"], dtype=np.float64)
    fwd = np.asarray(axes["forward"], dtype=np.float64)
    eye_dir = {"front": fwd, "back": -fwd, "left": -right, "right": right}[view]
    look = normalize(-eye_dir)
    cam_right = np.cross(look, up)
    if float(np.linalg.norm(cam_right)) < 1e-8:
        cam_right = np.cross(look, fwd)
    cam_right = normalize(cam_right)
    cam_up = normalize(np.cross(cam_right, look))
    return look, cam_right, cam_up


def pitch_down(look: np.ndarray, cam_up: np.ndarray, deg: float) -> tuple[np.ndarray, np.ndarray]:
    """Rotate a view basis down by `deg` about the unchanged camera right axis.

    A level orthographic camera sees a horizontal plane exactly edge-on, so a
    floor drawn under the character collapses to a line. Pitching down opens the
    plane out without touching the horizontal framing.
    """
    t = np.radians(deg)
    return (
        normalize(look * np.cos(t) - cam_up * np.sin(t)),
        normalize(cam_up * np.cos(t) + look * np.sin(t)),
    )


def build_camera(
    axes: dict,
    view: str,
    points: np.ndarray,
    width: int,
    height: int,
    *,
    fill: float = 0.82,
    pitch_deg: float = 0.0,
) -> Camera:
    """Fixed camera framing every point of the whole sequence.

    `points` is the full set of world points over all frames, so the framing is
    computed once. Nothing is re-centred per frame.
    """
    look, cam_right, cam_up = view_basis(axes, view)
    if pitch_deg:
        look, cam_up = pitch_down(look, cam_up, pitch_deg)
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    u = pts @ cam_right
    v = pts @ cam_up
    center_u = 0.5 * (float(u.min()) + float(u.max()))
    center_v = 0.5 * (float(v.min()) + float(v.max()))
    center = center_u * cam_right + center_v * cam_up
    span_u = max(float(u.max() - u.min()), 1e-3)
    span_v = max(float(v.max() - v.min()), 1e-3)
    scale = fill * min(width / span_u, height / span_v)
    return Camera(
        view=view,
        look=look,
        cam_right=cam_right,
        cam_up=cam_up,
        center=center,
        scale=scale,
        width=width,
        height=height,
    )


def build_perspective_camera(
    axes: dict,
    points: np.ndarray,
    width: int,
    height: int,
    *,
    fov_deg: float = 28.0,
    azimuth_deg: float = 0.0,
    elevation_deg: float = 10.0,
    fill: float = 0.94,
    iterations: int = 12,
) -> PerspectiveCamera:
    """Pinhole camera orbiting the sequence, framed on every point of it.

    azimuth turns the eye around the character's up axis from dead ahead;
    elevation lifts it above the floor. The eye distance and the aim point are
    then solved together so the whole clip fits, since with perspective the
    framing depends on where the eye is and not on a scale alone.
    """
    up = normalize(np.asarray(axes["up"], dtype=np.float64))
    fwd = normalize(np.asarray(axes["forward"], dtype=np.float64))
    right = normalize(np.asarray(axes["right"], dtype=np.float64))

    az, el = np.radians(azimuth_deg), np.radians(elevation_deg)
    offset = normalize(np.cos(el) * (np.cos(az) * fwd + np.sin(az) * right) + np.sin(el) * up)
    look = -offset
    cam_right = normalize(np.cross(look, up))
    cam_up = normalize(np.cross(cam_right, look))
    focal = (height * 0.5) / np.tan(np.radians(fov_deg) * 0.5)

    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    target = 0.5 * (pts.min(axis=0) + pts.max(axis=0))
    dist = float(np.linalg.norm(pts.max(axis=0) - pts.min(axis=0))) * 3.0

    def place(t: np.ndarray, d: float) -> PerspectiveCamera:
        return PerspectiveCamera(t + offset * d, look, cam_right, cam_up,
                                 float(focal), width, height)

    for _ in range(iterations):
        cam = place(target, dist)
        uv = cam.project(pts)
        lo, hi = uv.min(axis=0), uv.max(axis=0)
        mid = 0.5 * (lo + hi)
        # The world point on the aim plane that lands on `mid`; aim there instead.
        target = target + ((mid[0] - width * 0.5) * cam_right
                           - (mid[1] - height * 0.5) * cam_up) * dist / focal
        dist *= max((hi[0] - lo[0]) / (fill * width), (hi[1] - lo[1]) / (fill * height))

    # Re-aiming and rescaling interact, so guarantee the fit rather than assume it.
    for _ in range(40):
        cam = place(target, dist)
        uv = cam.project(pts)
        if (uv.min(axis=0) >= 0.0).all() and (uv.max(axis=0) < (width, height)).all():
            break
        dist *= 1.02
    return place(target, dist)


def content_panel_size(
    axes: dict,
    view: str,
    points: np.ndarray,
    height: int,
    *,
    min_w: int = 560,
    max_w: int = 1280,
) -> tuple[int, int]:
    """Panel shape matching what the sequence actually sweeps out.

    The camera stays fixed; this only stops a wandering character from being
    rendered into a panel whose aspect leaves most of it empty.
    """
    _, cam_right, cam_up = view_basis(axes, view)
    pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    span_u = max(float(np.ptp(pts @ cam_right)), 1e-3)
    span_v = max(float(np.ptp(pts @ cam_up)), 1e-3)
    width = int(round(height * span_u / span_v))
    width = int(np.clip(width, min_w, max_w))
    return width + width % 2, height + height % 2


def edge_bgr(a: str, b: str) -> tuple[int, int, int]:
    token = f"{a}_{b}".lower()
    if "left" in token:
        return LEFT_BGR
    if "right" in token:
        return RIGHT_BGR
    return TORSO_BGR


def blank_panel(width: int, height: int) -> np.ndarray:
    return np.full((height, width, 3), BG_BGR, dtype=np.uint8)


@dataclass(frozen=True)
class Ground:
    """A square patch of floor the character is standing on.

    `y` is a world height, so panels sharing a camera and a Ground put their
    floors on the same pixel rows and read as one surface. The patch is wide
    enough that under perspective its far edge crowds the vanishing point.
    """

    y: float
    cx: float
    cz: float
    extent: float = 9.0
    step: float = 0.5

    def corners(self) -> np.ndarray:
        e = self.extent
        return np.array([
            (self.cx - e, self.y, self.cz - e),
            (self.cx + e, self.y, self.cz - e),
            (self.cx + e, self.y, self.cz + e),
            (self.cx - e, self.y, self.cz + e),
        ], dtype=np.float64)

    def lines(self) -> np.ndarray:
        """Grid lines as world endpoint pairs, shape (n, 2, 3)."""
        e = self.extent
        ticks = np.arange(-e, e + 1e-9, self.step)
        segs = [((self.cx + t, self.y, self.cz - e), (self.cx + t, self.y, self.cz + e))
                for t in ticks]
        segs += [((self.cx - e, self.y, self.cz + t), (self.cx + e, self.y, self.cz + t))
                 for t in ticks]
        return np.asarray(segs, dtype=np.float64)


def ground_backdrop(cam, ground: Ground, width: int, height: int,
                    theme: Theme = DARK_THEME) -> np.ndarray:
    """The floor drawn once. Camera and floor are both fixed, so frames copy this."""
    import cv2

    img = np.full((height, width, 3), theme.bg, dtype=np.uint8)

    quad = cam.clip_near(ground.corners())
    if len(quad) >= 3:
        poly = np.rint(cam.project(quad)).astype(np.int32)
        mask = np.zeros((height, width), dtype=np.uint8)
        cv2.fillPoly(mask, [poly], 255, cv2.LINE_8)
        top, bottom = float(poly[:, 1].min()), float(poly[:, 1].max())
        t = np.clip((np.arange(height) - top) / max(bottom - top, 1.0), 0.0, 1.0)[:, None]
        ramp = (np.asarray(theme.floor_far, dtype=np.float64) * (1.0 - t)
                + np.asarray(theme.floor_near, dtype=np.float64) * t)
        img = np.where(mask[:, :, None] > 0, ramp[:, None, :], img).astype(np.uint8)

    segs = ground.lines()
    d = cam.depth(segs.mean(axis=1))
    span = max(float(np.ptp(d)), 1e-6)
    drawn: list[float] = []
    for i in np.argsort(-d):
        clipped = cam.clip_segment(segs[i, 0], segs[i, 1])
        if clipped is None:
            continue
        a, b = (cam.project(p)[0] for p in clipped)
        if max(abs(a[0] - b[0]), abs(a[1] - b[1])) < 3.0:
            continue
        # Lines crowding the vanishing point would fuse into a solid band.
        if abs(a[1] - b[1]) < 2.0:
            row = 0.5 * (a[1] + b[1])
            if any(abs(row - r) < 2.0 for r in drawn):
                continue
            drawn.append(row)
        near = float(np.clip((d[i] - d.min()) / span, 0.0, 1.0))
        far = np.asarray(theme.floor_far, dtype=np.float64)
        colour = far + (np.asarray(theme.grid, dtype=np.float64) - far) * (0.35 + 0.65 * near)
        cv2.line(img, tuple(np.rint(a).astype(int)), tuple(np.rint(b).astype(int)),
                 tuple(int(round(v)) for v in colour), 1, cv2.LINE_AA)
    return img


def draw_shadow(img: np.ndarray, cam, pts: np.ndarray, ground: Ground,
                theme: Theme = DARK_THEME) -> None:
    """The figure flattened onto the floor: an overhead light's cast shadow."""
    import cv2

    flat = np.asarray(pts, dtype=np.float64).reshape(-1, 3).copy()
    flat[:, 1] = ground.y
    hull = cv2.convexHull(np.rint(cam.project(flat)).astype(np.int32))
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(mask, hull, 255, cv2.LINE_8)
    mask = cv2.GaussianBlur(mask, (0, 0), 9)
    m = (mask.astype(np.float64) / 255.0 * theme.shadow_alpha)[:, :, None]
    blended = (img.astype(np.float64) * (1.0 - m)
               + np.asarray(theme.shadow, dtype=np.float64) * m)
    img[:] = np.clip(blended, 0, 255).astype(np.uint8)


def draw_skeleton(
    img: np.ndarray,
    pos: dict[str, np.ndarray],
    edges: list[tuple[str, str]],
    cam,
    thickness: int = 3,
    joint_bgr: tuple[int, int, int] = (242, 242, 242),
) -> None:
    import cv2

    names = list(pos.keys())
    uv = cam.project(np.stack([pos[n] for n in names]))
    px = {n: (int(round(uv[i, 0])), int(round(uv[i, 1]))) for i, n in enumerate(names)}
    for a, b in edges:
        if a in px and b in px:
            cv2.line(img, px[a], px[b], edge_bgr(a, b), thickness, cv2.LINE_AA)
    for p in px.values():
        cv2.circle(img, p, 3, joint_bgr, -1, cv2.LINE_AA)


def draw_mesh(
    img: np.ndarray,
    vertices: list[np.ndarray],
    faces: list[np.ndarray],
    colors: list[np.ndarray],
    cam: Camera,
    ambient: float = 0.30,
) -> None:
    """Back-to-front painter fill with Lambert shading from a head-on key light.

    A colour entry is either one BGR for the whole mesh or one per triangle.
    `ambient` is the floor of the shading term: on a near-black texture the lit
    side already sits low, so too little of it crushes the whole part to black.
    """
    import cv2

    polys: list[np.ndarray] = []
    shades: list[np.ndarray] = []
    depths: list[np.ndarray] = []
    light = -cam.look

    for verts, face, base in zip(vertices, faces, colors):
        uv = cam.project(verts)
        z = cam.depth(verts)
        v0, v1, v2 = face[:, 0], face[:, 1], face[:, 2]
        p0, p1, p2 = verts[v0], verts[v1], verts[v2]
        normals = np.cross(p1 - p0, p2 - p0)
        nlen = np.linalg.norm(normals, axis=1, keepdims=True)
        normals = normals / np.where(nlen < 1e-12, 1.0, nlen)
        facing = normals @ light
        keep = facing > 0.0
        if not np.any(keep):
            continue
        lambert = np.clip(np.abs(facing[keep]), 0.0, 1.0)
        shade = ambient + (1.0 - ambient) * lambert
        tri = np.stack([uv[v0[keep]], uv[v1[keep]], uv[v2[keep]]], axis=1)
        polys.append(np.rint(tri).astype(np.int32))
        tint = np.asarray(base, dtype=np.float64)
        tint = tint[None, :] if tint.ndim == 1 else tint[keep]
        shades.append(shade[:, None] * tint)
        depths.append((z[v0[keep]] + z[v1[keep]] + z[v2[keep]]) / 3.0)

    if not polys:
        return
    tri = np.concatenate(polys, axis=0)
    rgb = np.clip(np.concatenate(shades, axis=0), 0, 255)
    depth = np.concatenate(depths, axis=0)

    order = np.argsort(-depth)
    tri = tri[order]
    rgb = rgb[order].astype(np.int32)
    for i in range(tri.shape[0]):
        cv2.fillConvexPoly(img, tri[i], (int(rgb[i, 0]), int(rgb[i, 1]), int(rgb[i, 2])), cv2.LINE_8)


def label_panel(img: np.ndarray, text: str, *, flagged: bool = False, height: int = 32) -> None:
    import cv2

    w = img.shape[1]
    cv2.rectangle(img, (0, 0), (w, height), PANEL_BAR_BGR, -1)
    color = FLAG_BGR if flagged else TEXT_BGR
    cv2.putText(img, text, (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1, cv2.LINE_AA)


def footer(img: np.ndarray, text: str, height: int = 28) -> None:
    import cv2

    h, w = img.shape[:2]
    cv2.rectangle(img, (0, h - height), (w, h), PANEL_BAR_BGR, -1)
    cv2.putText(img, text, (10, h - 9), cv2.FONT_HERSHEY_SIMPLEX, 0.48, MUTED_BGR, 1, cv2.LINE_AA)


def hstack_panels(panels: list[np.ndarray]) -> np.ndarray:
    import cv2

    grid = np.hstack(panels)
    x = 0
    for panel in panels[:-1]:
        x += panel.shape[1]
        cv2.line(grid, (x, 0), (x, grid.shape[0]), (40, 40, 44), 1)
    return grid


def fit_letterbox(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    import cv2

    out = np.full((height, width, 3), BG_BGR, dtype=np.uint8)
    if frame is None:
        return out
    h, w = frame.shape[:2]
    s = min(width / w, height / h)
    nw, nh = max(1, int(round(w * s))), max(1, int(round(h * s)))
    resized = cv2.resize(frame, (nw, nh), interpolation=cv2.INTER_AREA)
    ox, oy = (width - nw) // 2, (height - nh) // 2
    out[oy:oy + nh, ox:ox + nw] = resized
    return out


COVER_SHIFT_X = 0.0


def cover_crop_box(
    src_w: int, src_h: int, width: int, height: int, shift_x: float = 0.0
) -> tuple[int, int, int, int]:
    """Crop of a src_w x src_h frame carrying the panel's aspect: x, y, w, h.

    shift_x slides the window by that fraction of its own width, negative = left,
    clamped so the window stays inside the frame.
    """
    crop_w = min(src_w, max(1, int(round(src_h * width / height))))
    crop_h = min(src_h, max(1, int(round(crop_w * height / width))))
    x0 = (src_w - crop_w) // 2 + int(round(shift_x * crop_w))
    y0 = (src_h - crop_h) // 2
    return max(0, min(src_w - crop_w, x0)), max(0, min(src_h - crop_h, y0)), crop_w, crop_h


def fit_cover(
    frame: np.ndarray, width: int, height: int, *, shift_x: float = COVER_SHIFT_X
) -> np.ndarray:
    """Crop to the panel's aspect, then fill it edge to edge.

    Letterboxing a 16:9 clip into a tall panel spends most of the panel on bars
    and leaves the dancer small next to the rendered panels beside it.
    """
    import cv2

    out = np.full((height, width, 3), BG_BGR, dtype=np.uint8)
    if frame is None:
        return out
    h, w = frame.shape[:2]
    x0, y0, crop_w, crop_h = cover_crop_box(w, h, width, height, shift_x)
    crop = frame[y0:y0 + crop_h, x0:x0 + crop_w]
    return cv2.resize(crop, (width, height), interpolation=cv2.INTER_AREA)


def write_video(path, frames_bgr: list[np.ndarray], fps: float) -> None:
    import cv2

    path.parent.mkdir(parents=True, exist_ok=True)
    h, w = frames_bgr[0].shape[:2]
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), float(fps), (w, h))
    if not writer.isOpened():
        raise RuntimeError(f"Cannot open VideoWriter for {path}")
    for frame in frames_bgr:
        writer.write(frame)
    writer.release()


def encode_h264(src, dst) -> bool:
    """Re-encode with ffmpeg when available so the clip plays in browsers."""
    import shutil
    import subprocess

    if shutil.which("ffmpeg") is None:
        return False
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(src),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
        str(dst),
    ]
    return subprocess.run(cmd, check=False).returncode == 0
