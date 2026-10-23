"""Interactive HTML view of diagnostics.json (`m2mr diagnose <run> --visualize`).

One self-contained file next to the GLB: the source video (or photo) beside
the character, both embedded and kept on the same frame, a timeline of every
issue, and a list you can click to jump to the worst frame. Parts in an active
issue turn red. three.js loads from a CDN, so the 3D view needs an internet
connection; the source, list, and timeline work offline.
"""

from __future__ import annotations

import base64
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from .diagnose import PARTS, SkinnedClip

_THREE = "https://cdn.jsdelivr.net/npm/three@0.160.0"
# The embedded copy of the source: small enough to keep the HTML a few MB.
_SOURCE_HEIGHT = 640
_SOURCE_FPS = 30


def _source_video(video: Path) -> tuple[dict, str] | None:
    """Small H.264 + AAC copy of the source, same timeline (frame k is at k / fps)."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        return None
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "source.mp4"
        cmd = [
            ffmpeg, "-v", "error", "-y", "-i", str(video),
            "-vf", f"fps={_SOURCE_FPS},scale=-2:'min({_SOURCE_HEIGHT},ih)'",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "28", "-preset", "veryfast",
            "-g", "15", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out),
        ]
        if subprocess.run(cmd, capture_output=True).returncode != 0 or not out.is_file():
            return None
        return {"kind": "video", "mime": "video/mp4"}, base64.b64encode(out.read_bytes()).decode("ascii")


def _source_image(image: Path) -> tuple[dict, str] | None:
    import cv2

    img = cv2.imread(str(image))
    if img is None:
        return None
    h, w = img.shape[:2]
    if h > _SOURCE_HEIGHT:
        img = cv2.resize(img, (round(w * _SOURCE_HEIGHT / h), _SOURCE_HEIGHT), interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return ({"kind": "image", "mime": "image/jpeg"}, base64.b64encode(buf.tobytes()).decode("ascii")) if ok else None


def source_media(run_dir: Path) -> tuple[dict, str]:
    """The run's input video or photo (from run.json), ready to embed; or a note why not."""
    try:
        run = json.loads((Path(run_dir) / "run.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"kind": "none", "note": "run.json not found, so the source video is unknown."}, ""
    for key, load in (("image", _source_image), ("video", _source_video)):
        src = run.get(key)
        if not src:
            continue
        if not Path(src).is_file():
            return {"kind": "none", "note": f"Source {key} not found: {src}"}, ""
        got = load(Path(src))
        if got is None:
            note = "ffmpeg is needed to embed the source video." if key == "video" else "Could not read the photo."
            return {"kind": "none", "note": note}, ""
        meta, b64 = got
        meta["name"] = Path(src).name
        return meta, b64
    return {"kind": "none", "note": "run.json lists no source video or photo."}, ""


def write_html_report(path: Path, glb_path: Path, report: dict, clip: SkinnedClip) -> Path:
    media, media_b64 = source_media(Path(glb_path).parent)
    payload = {
        "report": report,
        "parts": list(PARTS),
        "media": media,
        # Body part per vertex, per skinned mesh node, in GLB vertex order.
        "meshes": [
            {"name": clip.names[p.mesh_node], "count": int(len(p.part)), "part": p.part.tolist()}
            for p in clip.primitives
        ],
    }
    glb_b64 = base64.b64encode(Path(glb_path).read_bytes()).decode("ascii")
    html = (_TEMPLATE
            .replace("__THREE__", _THREE)
            .replace("__DATA__", json.dumps(payload, separators=(",", ":")))
            .replace("__MEDIA__", media_b64)
            .replace("__GLB__", glb_b64))
    path = Path(path)
    path.write_text(html, encoding="utf-8")
    return path


_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Motion2MixamoRig · Self-Intersection Diagnostics</title>
<style>
  :root {
    --bg:#121212; --panel:#1f1f1f; --head:#2a2a2a; --field:#151515; --control:#333333; --control-hi:#3d3d3d;
    --border:#000000; --edge:#3a3a3a; --line:#2c2c2c;
    --text:#cfcfcf; --bright:#f0f0f0; --muted:#8a8a8a; --dim:#5f5f5f;
    --green:#76b900; --green-hi:#8fd400; --green-sel:rgba(118,185,0,.16);
    --red:#f0524f; --red-sel:rgba(240,82,79,.16);
    --sans: "NVIDIA Sans", "Helvetica Neue", Arial, sans-serif;
    --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  }
  * { box-sizing:border-box; }
  html, body { height:100%; }
  body { margin:0; font:12px/1.4 var(--sans); color:var(--text); background:var(--bg); display:flex; flex-direction:column; overflow:hidden; }
  button, input { font:inherit; color:inherit; }
  button:focus { outline:none; }
  button:focus-visible { outline:1px solid var(--green); outline-offset:1px; }

  /* Application bar */
  #titlebar { flex:0 0 auto; height:40px; display:flex; align-items:stretch; background:#000; border-bottom:1px solid var(--edge); }
  .brand { display:flex; align-items:center; gap:10px; padding:0 16px 0 0; white-space:nowrap; }
  .brand .bar { width:4px; align-self:stretch; background:var(--green); }
  .brand .name { font-weight:700; letter-spacing:.06em; color:var(--bright); font-size:13px; }
  .brand .sep { width:1px; height:16px; background:var(--edge); }
  .brand .app { color:var(--muted); font-size:12px; letter-spacing:.02em; }
  #meta { display:flex; align-items:stretch; flex:1; min-width:0; overflow:hidden; border-left:1px solid var(--line); }
  .field { display:flex; flex-direction:column; justify-content:center; padding:0 14px; border-right:1px solid var(--line); white-space:nowrap; }
  .field .k { font-size:9.5px; letter-spacing:.1em; text-transform:uppercase; color:var(--dim); }
  .field .v { font-family:var(--mono); font-size:11.5px; color:var(--text); }
  #status { display:flex; align-items:center; gap:8px; padding:0 16px; white-space:nowrap; font-weight:700; letter-spacing:.04em; text-transform:uppercase; font-size:11px; border-left:1px solid var(--line); }
  #status::before { content:""; width:8px; height:8px; background:currentColor; }
  #status.alert { color:var(--red); }
  #status.ok { color:var(--green); }

  /* Docked panels, 1 px apart */
  #work { flex:1 1 auto; min-height:0; display:grid; grid-template-columns:minmax(0,1fr) 340px; gap:1px; background:var(--border); }
  #left { min-width:0; min-height:0; display:flex; flex-direction:column; gap:1px; }
  .panel { background:var(--panel); min-height:0; overflow:hidden; }
  .phead { flex:0 0 auto; height:26px; display:flex; align-items:center; gap:8px; padding:0 10px; background:var(--head); border-bottom:1px solid var(--border); font-size:10.5px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--text); user-select:none; white-space:nowrap; }
  .phead .sub { font-weight:400; letter-spacing:.02em; text-transform:none; color:var(--muted); font-size:11px; overflow:hidden; text-overflow:ellipsis; }
  .phead[data-toggle] { cursor:pointer; }
  .phead[data-toggle]:hover { background:#303030; }
  .phead .tri { color:var(--muted); width:9px; font-size:9px; }
  .phead .count { margin-left:auto; font-family:var(--mono); font-weight:400; letter-spacing:0; color:var(--muted); }

  #viewports { flex:1 1 auto; min-height:0; display:flex; gap:1px; background:var(--border); }
  .vp { position:relative; min-width:0; display:flex; flex-direction:column; background:var(--panel); }
  .vp .body { position:relative; flex:1 1 auto; min-height:0; overflow:hidden; }
  #source { flex:0 0 auto; max-width:46%; }
  #source .body { background:#0a0a0a; display:flex; align-items:center; justify-content:center; }
  #source video, #source img { display:block; width:100%; height:100%; object-fit:contain; }
  #source .note { color:var(--muted); padding:16px; text-align:center; width:240px; }
  #view { flex:1 1 auto; }
  #view canvas { display:block; }
  .hint { position:absolute; top:8px; right:10px; z-index:2; font-size:10.5px; color:var(--dim); pointer-events:none; }
  .caption { position:absolute; left:10px; bottom:10px; z-index:2; pointer-events:none; padding:5px 10px; background:rgba(0,0,0,.72); border-left:3px solid var(--green); font-size:12px; }
  .caption.bad { border-left-color:var(--red); }
  .caption .bad { color:var(--red); font-weight:700; }
  .caption .ok { color:var(--green); font-weight:700; }
  #viewMsg { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; color:var(--muted); text-align:center; padding:24px; }

  /* Timeline */
  #dock { flex:0 0 auto; display:flex; flex-direction:column; }
  .toolbar { display:flex; align-items:center; gap:4px; padding:5px 8px; border-bottom:1px solid var(--border); background:var(--panel); flex-wrap:wrap; }
  .btn { height:24px; min-width:26px; padding:0 8px; display:inline-flex; align-items:center; justify-content:center; gap:6px; background:var(--control); border:1px solid #444; border-radius:2px; color:var(--text); cursor:pointer; font-size:11.5px; }
  .btn:hover { background:var(--control-hi); border-color:#555; color:var(--bright); }
  .btn:disabled { opacity:.35; cursor:default; }
  .btn svg { width:11px; height:11px; fill:currentColor; }
  .btn.primary { background:var(--green); border-color:var(--green); color:#000; font-weight:700; min-width:72px; }
  .btn.primary:hover { background:var(--green-hi); border-color:var(--green-hi); color:#000; }
  .btn.on { border-color:var(--green); color:var(--green); }
  .vsep { width:1px; height:18px; background:var(--edge); margin:0 6px; }
  .framebox { display:inline-flex; align-items:center; gap:6px; height:24px; padding:0 8px; background:var(--field); border:1px solid #444; border-radius:2px; color:var(--muted); font-size:11px; }
  .framebox input { width:44px; border:none; outline:none; text-align:right; font-family:var(--mono); font-size:12px; color:var(--bright); background:transparent; }
  .framebox:focus-within { border-color:var(--green); }
  .framebox .mono { font-family:var(--mono); }
  .grow { flex:1; }
  input[type=range] { -webkit-appearance:none; appearance:none; background:transparent; width:80px; }
  input[type=range]::-webkit-slider-runnable-track { height:3px; background:#4a4a4a; }
  input[type=range]::-webkit-slider-thumb { -webkit-appearance:none; width:8px; height:14px; margin-top:-5.5px; border-radius:1px; background:var(--text); }
  input[type=range]::-moz-range-track { height:3px; background:#4a4a4a; }
  input[type=range]::-moz-range-thumb { width:8px; height:14px; border-radius:1px; background:var(--text); border:none; }
  #nowbar { display:flex; align-items:center; gap:6px; padding:0 10px; height:28px; border-bottom:1px solid var(--line); overflow:hidden; white-space:nowrap; }
  #nowbar .lab { font-size:9.5px; letter-spacing:.1em; text-transform:uppercase; color:var(--dim); margin-right:4px; }
  .tag { display:inline-block; padding:1px 7px; border:1px solid rgba(240,82,79,.55); background:var(--red-sel); color:#ff8a87; font-size:11px; border-radius:1px; }
  .clean { color:var(--green); font-size:11.5px; }
  #tlwrap { max-height:26vh; overflow-y:auto; overflow-x:hidden; background:var(--panel); }
  #timeline { width:100%; display:block; cursor:pointer; }

  /* Inspector */
  #right { display:flex; flex-direction:column; }
  .props { display:grid; grid-template-columns:118px 1fr; border-bottom:1px solid var(--border); }
  .props > div { padding:5px 10px; border-bottom:1px solid var(--line); }
  .props .k { color:var(--muted); }
  .props .v { color:var(--bright); font-family:var(--mono); font-size:11.5px; }
  .props .v.bad { color:var(--red); }
  .filters { display:flex; padding:6px 8px; border-bottom:1px solid var(--line); }
  .filters button { flex:1; height:22px; background:var(--control); border:1px solid #444; margin-left:-1px; color:var(--muted); cursor:pointer; font-size:11px; }
  .filters button:first-child { margin-left:0; border-radius:2px 0 0 2px; }
  .filters button:last-child { border-radius:0 2px 2px 0; }
  .filters button:hover { color:var(--bright); }
  .filters button.on { background:#3a4a22; border-color:var(--green); color:var(--bright); position:relative; z-index:1; }
  #issuesBody { flex:1 1 auto; min-height:0; display:flex; flex-direction:column; }
  #issues { flex:1 1 auto; overflow:auto; }
  .issue { position:relative; padding:7px 10px 7px 12px; border-bottom:1px solid var(--line); border-left:3px solid transparent; cursor:pointer; }
  .issue:hover { background:#262626; }
  .issue.sel { background:var(--green-sel); border-left-color:var(--green); }
  .issue .t { color:var(--bright); padding-right:70px; }
  .issue .d { position:absolute; top:7px; right:10px; font-family:var(--mono); font-weight:700; color:var(--red); }
  .issue.restpose .d { color:var(--muted); }
  .issue .m { color:var(--muted); font-size:11px; margin-top:2px; }
  .issue .r { color:var(--dim); font-size:10.5px; margin-top:2px; font-family:var(--mono); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .issue .badge { display:inline-block; margin-top:5px; font-size:10px; letter-spacing:.06em; text-transform:uppercase; padding:0 5px; border:1px solid var(--edge); color:var(--muted); }
  .empty { padding:18px; text-align:center; color:var(--muted); }
  #method { margin:0; padding:8px 12px 10px 26px; color:var(--muted); font-size:11.5px; line-height:1.55; max-height:30vh; overflow:auto; }
  #method li { margin:4px 0; }
  #method b { color:var(--text); }
  .collapsed + * { display:none !important; }
  ::-webkit-scrollbar { width:8px; height:8px; } ::-webkit-scrollbar-track { background:var(--panel); }
  ::-webkit-scrollbar-thumb { background:#444; } ::-webkit-scrollbar-thumb:hover { background:#555; }
  @media (max-width:980px) { body { overflow:auto; height:auto; } #work { grid-template-columns:1fr; } #viewports { height:60vh; } #meta { display:none; } }
</style>
<script type="importmap">{"imports":{"three":"__THREE__/build/three.module.js","three/addons/":"__THREE__/examples/jsm/"}}</script>
</head>
<body>
<div id="titlebar">
  <div class="brand"><span class="bar"></span><span class="name">MOTION2MIXAMORIG</span><span class="sep"></span><span class="app">Self-Intersection Diagnostics</span></div>
  <div id="meta"></div>
  <div id="status"></div>
</div>

<div id="work">
  <div id="left">
    <div id="viewports">
      <div class="vp" id="source">
        <div class="phead">Source <span class="sub" id="srcLabel"></span></div>
        <div class="body"></div>
      </div>
      <div class="vp" id="view">
        <div class="phead">Viewport <span class="sub">Character</span></div>
        <div class="body" id="viewBody">
          <span class="hint">LMB orbit · Wheel zoom</span>
          <div class="caption" id="caption"></div>
          <div id="viewMsg">Loading the 3D view…</div>
        </div>
      </div>
    </div>

    <div class="panel" id="dock">
      <div class="phead">Timeline</div>
      <div class="toolbar">
        <button class="btn" id="first" title="First frame"><svg viewBox="0 0 16 16"><path d="M3 2h2v12H3zM13 2v12L6 8z"/></svg></button>
        <button class="btn" id="prev" title="Previous frame (←)"><svg viewBox="0 0 16 16"><path d="M11 2v12L4 8z"/></svg></button>
        <button class="btn primary" id="play" title="Play / Pause (Space)"></button>
        <button class="btn" id="next" title="Next frame (→)"><svg viewBox="0 0 16 16"><path d="M5 2v12l7-6z"/></svg></button>
        <button class="btn" id="last" title="Last frame"><svg viewBox="0 0 16 16"><path d="M11 2h2v12h-2zM3 2v12l7-6z"/></svg></button>
        <span class="vsep"></span>
        <span class="framebox">FRAME <input id="frameField" inputmode="numeric" title="Type a frame and press Enter"> <span class="mono" id="frameTotal"></span> <span class="mono" id="timeInfo"></span></span>
        <div class="grow"></div>
        <button class="btn" id="sound" title="Sound of the original video"></button>
        <input id="volume" type="range" min="0" max="1" step="0.05" value="0.8" title="Volume">
      </div>
      <div id="nowbar"><span class="lab">Active</span><span id="now"></span></div>
      <div id="tlwrap"><canvas id="timeline"></canvas></div>
    </div>
  </div>

  <div class="panel" id="right">
    <div class="phead" data-toggle><span class="tri">▼</span>Summary</div>
    <div class="props" id="summary"></div>
    <div class="phead" data-toggle><span class="tri">▼</span>Issues<span class="count" id="issueCount"></span></div>
    <div id="issuesBody">
      <div class="filters" id="filters">
        <button class="on" data-f="all">All pairs</button>
        <button data-f="motion">From motion</button>
        <button data-f="now">This frame</button>
      </div>
      <div id="issues"></div>
    </div>
    <div class="phead collapsed" data-toggle><span class="tri">▶</span>Method</div>
    <ul id="method"></ul>
  </div>
</div>

<script type="application/json" id="data">__DATA__</script>
<script type="text/plain" id="media">__MEDIA__</script>
<script type="text/plain" id="glb">__GLB__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const R = D.report, N = R.frame_count, FPS = R.fps;
const $ = id => document.getElementById(id);
const label = p => p.replace(/_/g, ' ');
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
const pairName = i => cap(i.parts.map(label).join(' ↔ '));
const fmtRange = ([a, b]) => a === b ? `${a}` : `${a}–${b}`;
let frame = 0, selected = -1, playing = false, filter = 'all';
window.diag = { setFrame: f => setFrame(f), onFrame: null };

const ICON = {
  play: '<svg viewBox="0 0 16 16"><path d="M4 2l10 6-10 6z"/></svg> PLAY',
  pause: '<svg viewBox="0 0 16 16"><path d="M3 2h4v12H3zM9 2h4v12H9z"/></svg> PAUSE',
  on: '<svg viewBox="0 0 16 16"><path d="M2 6h3l4-3v10l-4-3H2zM11 5.5a3.5 3.5 0 010 5l-.8-.8a2.4 2.4 0 000-3.4zM12.6 3.9a5.8 5.8 0 010 8.2l-.8-.8a4.7 4.7 0 000-6.6z"/></svg> Audio',
  off: '<svg viewBox="0 0 16 16"><path d="M2 6h3l4-3v10l-4-3H2zM11 6.2l.8-.8 1.6 1.6 1.6-1.6.8.8L14.2 8l1.6 1.6-.8.8-1.6-1.6-1.6 1.6-.8-.8L12.6 8z"/></svg> Muted',
};

// Collapsible panels.
document.querySelectorAll('[data-toggle]').forEach(h => h.onclick = () => {
  h.classList.toggle('collapsed'); h.querySelector('.tri').textContent = h.classList.contains('collapsed') ? '▶' : '▼';
  setTimeout(drawTimeline, 0);
});

// Original video / photo, on the same timeline (frame k at k / fps).
const M = D.media, src = $('source'), srcBody = src.querySelector('.body');
let video = null;
if (M.kind === 'video' || M.kind === 'image') {
  const el = document.createElement(M.kind === 'video' ? 'video' : 'img');
  el.src = `data:${M.mime};base64,` + $('media').textContent.trim();
  if (M.kind === 'video') { video = el; el.muted = true; el.playsInline = true; el.preload = 'auto'; }
  el.addEventListener(video ? 'loadedmetadata' : 'load', () => {
    const w = el.videoWidth || el.naturalWidth, h = el.videoHeight || el.naturalHeight;
    if (w && h) { src.style.aspectRatio = `${w} / ${h}`; window.dispatchEvent(new Event('resize')); }
    if (video) video.currentTime = frame / FPS;
  });
  srcBody.append(el);
  $('srcLabel').textContent = M.name;
} else {
  src.style.width = '260px';
  const n = document.createElement('div'); n.className = 'note'; n.textContent = M.note || 'No source video.'; srcBody.append(n);
}

// Sound: off by default (browsers block autoplay with sound); one click turns it on.
function showSound() { $('sound').innerHTML = video && !video.muted ? ICON.on : ICON.off; $('sound').classList.toggle('on', !!video && !video.muted); }
if (video) {
  video.volume = +$('volume').value;
  $('sound').onclick = () => { video.muted = !video.muted; showSound(); };
  $('volume').oninput = e => { video.volume = +e.target.value; if (video.muted && video.volume > 0) { video.muted = false; showSound(); } };
} else { $('sound').disabled = true; $('volume').disabled = true; }
showSound();

// Application bar and summary.
const S = R.summary.self_intersection;
const field = (k, v) => `<div class="field"><span class="k">${k}</span><span class="v">${v}</span></div>`;
$('meta').innerHTML = [field('Source', R.source), field('Frames', `${N} @ ${FPS} fps`), field('Threshold', `${R.threshold_cm} cm`)].join('');
$('status').className = S.issue_count ? 'alert' : 'ok';
$('status').textContent = S.issue_count ? `${S.issue_count} intersections · max ${S.max_depth_cm} cm` : 'No intersection';
const kv = [
  ['Check', 'Self-intersection'],
  ['Part pairs', S.issue_count, S.issue_count > 0],
  ['Frames affected', `${S.frame_count} / ${N} (${(100 * S.frame_count / Math.max(1, N)).toFixed(1)}%)`, S.frame_count > 0],
  ['Max depth', `${S.max_depth_cm} cm`, S.max_depth_cm > 0],
  ['Frame numbers', 'Blender, first = 0'],
  ['Generated', R.generated.replace('T', ' ')],
];
$('summary').innerHTML = kv.map(([k, v, bad]) => `<div class="k">${k}</div><div class="v${bad ? ' bad' : ''}">${v}</div>`).join('');
$('frameTotal').textContent = `/ ${N - 1}`;
for (const [k, v] of Object.entries(R.method)) { const li = document.createElement('li'); li.innerHTML = `<b>${cap(k.replace(/_/g, ' '))}.</b> `; li.append(v); $('method').append(li); }

const inRange = (i, f) => i.ranges.some(([a, b]) => f >= a && f <= b);
const visible = () => R.issues.filter(i =>
  filter === 'all' || (filter === 'motion' && !i.also_in_rest_pose) || (filter === 'now' && inRange(i, frame)));

function renderList() {
  const box = $('issues'), items = visible(); box.innerHTML = '';
  $('issueCount').textContent = `${items.length}`;
  if (!items.length) { box.innerHTML = `<div class="empty">${filter === 'now' ? 'No intersection on this frame.' : 'No issues to show.'}</div>`; return; }
  items.forEach(i => {
    const idx = R.issues.indexOf(i), el = document.createElement('div');
    el.className = 'issue' + (i.also_in_rest_pose ? ' restpose' : '') + (idx === selected ? ' sel' : '');
    el.innerHTML = '<div class="t"></div><div class="d"></div><div class="m"></div><div class="r"></div>';
    el.querySelector('.t').textContent = pairName(i);
    el.querySelector('.d').textContent = `${i.max_depth_cm.toFixed(2)} cm`;
    el.querySelector('.m').textContent = `${i.frame_count} frame${i.frame_count === 1 ? '' : 's'} · worst at frame ${i.worst_frame}`;
    el.querySelector('.r').textContent = i.ranges.map(fmtRange).join(', ');
    if (i.also_in_rest_pose) { const b = document.createElement('span'); b.className = 'badge'; b.textContent = 'Also in rest pose'; el.append(b); }
    el.onclick = () => { stop(); selected = idx; setFrame(i.worst_frame); renderList(); };
    box.append(el);
  });
}
document.querySelectorAll('#filters button').forEach(b => b.onclick = () => {
  filter = b.dataset.f; document.querySelectorAll('#filters button').forEach(x => x.classList.toggle('on', x === b)); renderList(); drawTimeline();
});

// Timeline: label column, ruler, one track per issue, green playhead.
const TL = { label: 180, ruler: 22, row: 20, pad: 12 };
function drawTimeline() {
  const c = $('timeline'), items = filter === 'now' ? R.issues : visible();
  const w = c.clientWidth || c.parentElement.clientWidth, h = TL.ruler + Math.max(1, items.length) * TL.row + 4;
  const dpr = window.devicePixelRatio || 1;
  c.width = w * dpr; c.height = h * dpr; c.style.height = h + 'px';
  const g = c.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
  const x0 = TL.label + TL.pad, x1 = w - TL.pad, x = f => x0 + (x1 - x0) * (N > 1 ? f / (N - 1) : 0);
  g.clearRect(0, 0, w, h);
  const font = '"NVIDIA Sans", "Helvetica Neue", Arial, sans-serif', mono = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace';
  g.fillStyle = '#262626'; g.fillRect(0, 0, w, TL.ruler);
  g.fillStyle = '#000'; g.fillRect(0, TL.ruler - 1, w, 1);
  g.fillStyle = '#1b1b1b'; g.fillRect(0, TL.ruler, TL.label, h - TL.ruler);
  g.fillStyle = '#000'; g.fillRect(TL.label, 0, 1, h);
  const pxPerFrame = (x1 - x0) / Math.max(1, N - 1);
  const major = [1, 5, 10, 25, 50, 100, 250, 500, 1000].find(s => s * pxPerFrame >= 60) || 1000;
  const minor = major >= 10 ? major / 5 : 1;
  g.font = `10px ${mono}`; g.textBaseline = 'top'; g.textAlign = 'center';
  for (let f = 0; f < N; f += minor) {
    const isMajor = f % major === 0, xx = Math.round(x(f)) + .5;
    g.strokeStyle = isMajor ? '#6a6a6a' : '#3e3e3e'; g.beginPath(); g.moveTo(xx, TL.ruler - (isMajor ? 8 : 4)); g.lineTo(xx, TL.ruler - 1); g.stroke();
    if (isMajor) { g.fillStyle = '#8a8a8a'; g.fillText(String(f), xx, 3); g.fillStyle = 'rgba(255,255,255,.035)'; g.fillRect(xx - .5, TL.ruler, 1, h - TL.ruler); }
  }
  g.textAlign = 'left';
  items.forEach((i, k) => {
    const y = TL.ruler + k * TL.row, idx = R.issues.indexOf(i), sel = idx === selected;
    if (sel) { g.fillStyle = 'rgba(118,185,0,.16)'; g.fillRect(0, y, w, TL.row); g.fillStyle = '#76b900'; g.fillRect(0, y, 3, TL.row); }
    else if (k % 2) { g.fillStyle = 'rgba(255,255,255,.02)'; g.fillRect(0, y, w, TL.row); }
    g.fillStyle = '#2c2c2c'; g.fillRect(0, y + TL.row - 1, w, 1);
    g.fillStyle = sel ? '#f0f0f0' : (i.also_in_rest_pose ? '#6a6a6a' : '#cfcfcf'); g.textBaseline = 'middle';
    g.font = `${sel ? 700 : 400} 11.5px ${font}`;
    let name = pairName(i); while (g.measureText(name).width > TL.label - 16 && name.length > 4) name = name.slice(0, -2) + '…';
    g.fillText(name, 10, y + TL.row / 2 + .5);
    g.fillStyle = i.also_in_rest_pose ? '#5a5a5a' : '#f0524f';
    for (const [a, b] of i.ranges) g.fillRect(Math.round(x(a)) - 1, y + 5, Math.max(3, Math.round(x(b) - x(a)) + 2), TL.row - 11);
  });
  const px = Math.round(x(frame)) + .5;
  g.strokeStyle = '#76b900'; g.lineWidth = 1; g.beginPath(); g.moveTo(px, TL.ruler - 2); g.lineTo(px, h); g.stroke();
  g.fillStyle = '#76b900'; g.fillRect(px - 17, 1, 34, TL.ruler - 4);
  g.fillStyle = '#000'; g.font = `700 10.5px ${mono}`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(String(frame), px, TL.ruler / 2 - 1); g.textAlign = 'left';

  c.onmousedown = e => {
    stop();
    const r = c.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
    if (mx < TL.label && my > TL.ruler) {
      const it = items[Math.floor((my - TL.ruler) / TL.row)];
      if (it) { selected = R.issues.indexOf(it); setFrame(it.worst_frame); renderList(); }
      return;
    }
    const seek = ev => setFrame(Math.round((ev.clientX - r.left - x0) / (x1 - x0) * (N - 1)));
    seek(e);
    const move = ev => seek(ev), up = () => { removeEventListener('mousemove', move); removeEventListener('mouseup', up); };
    addEventListener('mousemove', move); addEventListener('mouseup', up);
  };
}

function setFrame(f, fromVideo = false) {
  frame = Math.max(0, Math.min(N - 1, f | 0));
  if (video && !fromVideo && video.readyState >= 1) video.currentTime = frame / FPS;
  if (document.activeElement !== $('frameField')) $('frameField').value = frame;
  $('timeInfo').textContent = `${(frame / FPS).toFixed(2)} s`;
  const now = R.issues.filter(i => inRange(i, frame));
  $('now').innerHTML = now.length ? '' : '<span class="clean">No intersection</span>';
  now.forEach(i => { const t = document.createElement('span'); t.className = 'tag'; t.textContent = pairName(i); $('now').append(t); });
  $('caption').className = 'caption' + (now.length ? ' bad' : '');
  $('caption').innerHTML = now.length ? `<span class="bad">${now.map(pairName).join(' · ')}</span>` : '<span class="ok">No intersection on this frame</span>';
  drawTimeline();
  if (filter === 'now') renderList();
  if (window.diag.onFrame) window.diag.onFrame(frame, now);
}

// Transport.
function setPlayIcon() { $('play').innerHTML = playing ? ICON.pause : ICON.play; }
function stop() { if (playing) togglePlay(); }
let last = 0, acc = 0;
function togglePlay() {
  playing = !playing; setPlayIcon();
  if (video) { playing ? video.play() : video.pause(); }
  last = performance.now(); if (playing) requestAnimationFrame(tick);
}
function tick(t) {
  if (!playing) return;
  if (video) {
    const f = Math.round(video.currentTime * FPS);   // the video is the clock
    if (video.ended || f >= N) { video.currentTime = 0; video.play(); setFrame(0); }
    else if (f !== frame) setFrame(f, true);
  } else {
    acc += (t - last) / 1000 * FPS; last = t;
    if (acc >= 1) { const step = Math.floor(acc); acc -= step; setFrame(frame + step >= N ? 0 : frame + step); }
  }
  requestAnimationFrame(tick);
}
$('play').onclick = togglePlay;
$('prev').onclick = () => { stop(); setFrame(frame - 1); };
$('next').onclick = () => { stop(); setFrame(frame + 1); };
$('first').onclick = () => { stop(); setFrame(0); };
$('last').onclick = () => { stop(); setFrame(N - 1); };
$('frameField').onkeydown = e => { if (e.key === 'Enter') { stop(); setFrame(parseInt(e.target.value, 10) || 0); e.target.blur(); } };
addEventListener('keydown', e => {
  if (e.target.id === 'frameField') return;
  if (e.code === 'Space') { e.preventDefault(); togglePlay(); }
  else if (e.key === 'ArrowLeft') { stop(); setFrame(frame - 1); }
  else if (e.key === 'ArrowRight') { stop(); setFrame(frame + 1); }
});
addEventListener('resize', drawTimeline);
setPlayIcon();
renderList();
setFrame(R.issues.length ? R.issues[0].worst_frame : 0);
</script>

<script type="module">
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const D = JSON.parse(document.getElementById('data').textContent);
const FPS = D.report.fps;
const view = document.getElementById('viewBody'), msg = document.getElementById('viewMsg');
const bytes = Uint8Array.from(atob(document.getElementById('glb').textContent.trim()), c => c.charCodeAt(0));

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(window.devicePixelRatio || 1);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
view.prepend(renderer.domElement);

// Dark viewport: grey void, metre grid on the floor, soft contact shadow.
const BG = 0x2b2b2b;
const scene = new THREE.Scene();
scene.background = new THREE.Color(BG);
scene.fog = new THREE.Fog(BG, 7, 22);
const camera = new THREE.PerspectiveCamera(35, 1, 0.01, 100);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
scene.add(new THREE.HemisphereLight(0xffffff, 0x3a3a3a, 1.6));
const sun = new THREE.DirectionalLight(0xffffff, 2.0);
sun.position.set(2.5, 6, 3); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048); sun.shadow.radius = 6;
Object.assign(sun.shadow.camera, { left: -2, right: 2, top: 2, bottom: -2, near: 0.5, far: 20 });
scene.add(sun); scene.add(sun.target);
const floor = new THREE.Group(); scene.add(floor);
const minor = new THREE.GridHelper(40, 400, 0x353535, 0x353535), major = new THREE.GridHelper(40, 40, 0x4a4a4a, 0x4a4a4a);
minor.position.y = 0.0005; major.position.y = 0.001;
const ground = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ opacity: 0.45 }));
ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true;
floor.add(minor, major, ground);

function size() { const w = view.clientWidth, h = view.clientHeight; renderer.setSize(w, h); camera.aspect = w / Math.max(1, h); camera.updateProjectionMatrix(); }
window.addEventListener('resize', size); size();

const BASE = new THREE.Color(0x9a9c9e), HOT = new THREE.Color(0xf0524f);
new GLTFLoader().parse(bytes.buffer, '', gltf => {
  msg.remove();
  scene.add(gltf.scene);
  const mixer = new THREE.AnimationMixer(gltf.scene);
  if (gltf.animations[0]) mixer.clipAction(gltf.animations[0]).play();

  // Matte grey character; parts in an issue on this frame turn red.
  const targets = [];
  gltf.scene.traverse(o => {
    if (o.isMesh) o.castShadow = true;
    if (!o.isSkinnedMesh) return;
    const pos = o.geometry.attributes.position;
    const info = D.meshes.find(m => m.name === o.name && m.count === pos.count) || D.meshes.find(m => m.count === pos.count);
    if (!info) return;
    const col = new Float32Array(pos.count * 3);
    for (let v = 0; v < pos.count; v++) { col[3 * v] = BASE.r; col[3 * v + 1] = BASE.g; col[3 * v + 2] = BASE.b; }
    o.geometry.setAttribute('color', new THREE.BufferAttribute(col, 3));
    o.material = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.7, metalness: 0 });
    o.frustumCulled = false;
    targets.push({ attr: o.geometry.attributes.color, part: info.part });
  });
  if (!targets.length) { const m = document.createElement('div'); m.id = 'viewMsg'; m.textContent = 'Could not match the mesh to the report.'; view.append(m); }

  function paint(active) {
    const hot = new Set();
    active.forEach(i => i.parts.forEach(p => hot.add(D.parts.indexOf(p))));
    for (const t of targets) {
      const a = t.attr.array;
      for (let v = 0; v < t.part.length; v++) {
        const c = hot.has(t.part[v]) ? HOT : BASE;
        a[3 * v] = c.r; a[3 * v + 1] = c.g; a[3 * v + 2] = c.b;
      }
      t.attr.needsUpdate = true;
    }
  }

  mixer.setTime(0); gltf.scene.updateMatrixWorld(true);
  const box = new THREE.Box3().setFromObject(gltf.scene), c = box.getCenter(new THREE.Vector3()), sz = box.getSize(new THREE.Vector3());
  floor.position.y = box.min.y;
  controls.target.copy(c);
  camera.position.copy(c).add(new THREE.Vector3(sz.y * 0.7, sz.y * 0.75, Math.max(sz.y, sz.x) * 2.2));
  controls.update();

  // Keep the shadow camera on the character (follow the hips bone) as it moves around.
  let hips = null; gltf.scene.traverse(o => { if (!hips && o.isBone && /hips$/i.test(o.name)) hips = o; });
  const follow = new THREE.Vector3();
  window.diag.onFrame = (f, active) => {
    mixer.setTime(f / FPS); paint(active);
    if (hips) { gltf.scene.updateMatrixWorld(true); hips.getWorldPosition(follow); } else follow.copy(c);
    sun.target.position.set(follow.x, box.min.y, follow.z); sun.position.set(follow.x + 2.5, box.min.y + 6, follow.z + 3);
  };
  window.diag.setFrame(+document.getElementById('frameField').value || 0);
  renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
}, err => { msg.textContent = 'Could not load the 3D view: ' + err; });
</script>
<script>
// three.js comes from a CDN; without a connection the module above never runs.
setTimeout(() => { const m = document.getElementById('viewMsg'); if (m && m.textContent.startsWith('Loading')) m.textContent = 'The 3D view needs an internet connection to load three.js. The video, timeline, and issue list work offline.'; }, 10000);
</script>
</body>
</html>
"""
