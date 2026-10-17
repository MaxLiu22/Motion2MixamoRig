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
<title>Motion2MixamoRig diagnostics</title>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg:#f5f5f6; --panel:#ffffff; --text:#222222; --heading:#111111; --subtle:#555555; --muted:#8a8a8a;
    --border:#dddddd; --line:#ececec; --soft:#f0f0f0; --green:#76b900; --green-dark:#4a7a00; --green-soft:#f1f8e4;
    --red:#e5484d; --red-soft:#fdecec; --rest:#b8b8b8;
    --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  }
  * { box-sizing:border-box; }
  html, body { height:100%; }
  body { margin:0; font:14px/1.45 "Google Sans", "Segoe UI", system-ui, -apple-system, sans-serif; color:var(--text); background:var(--bg); display:flex; flex-direction:column; overflow:hidden; }
  button, input { font:inherit; color:inherit; }

  /* Title bar */
  #titlebar { flex:0 0 auto; height:56px; display:flex; align-items:center; gap:16px; padding:0 18px; background:rgba(255,255,255,.92); backdrop-filter:blur(10px); border-bottom:1px solid var(--border); }
  .brand { display:flex; align-items:center; gap:10px; font-weight:700; color:var(--heading); white-space:nowrap; font-size:16px; }
  .brand .g { color:var(--green); }
  .mark { width:22px; height:22px; border-radius:6px; background:var(--green); position:relative; flex:0 0 auto; }
  .mark::after { content:""; position:absolute; inset:6px; border:2px solid #fff; border-radius:50%; }
  #meta { display:flex; gap:8px; flex:1; min-width:0; overflow:hidden; }
  .pill { display:inline-flex; align-items:center; gap:6px; padding:5px 14px; border-radius:20px; border:1px solid var(--border); color:var(--subtle); background:#fff; white-space:nowrap; font-size:13px; }
  .pill .k { color:var(--muted); }
  .pill.solid { background:var(--green); border-color:var(--green); color:#000; font-weight:500; }
  .pill.alert { background:var(--red-soft); border-color:#f4b6b8; color:#b42328; font-weight:500; }

  /* Workspace */
  #work { flex:1 1 auto; min-height:0; display:grid; grid-template-columns:minmax(0,1fr) 360px; gap:12px; padding:12px; }
  #left { min-width:0; min-height:0; display:flex; flex-direction:column; gap:12px; }
  .card { background:var(--panel); border:1px solid var(--line); border-radius:16px; box-shadow:0 4px 18px rgba(0,0,0,.06); overflow:hidden; }

  #viewports { flex:1 1 auto; min-height:0; display:flex; }
  .vp { position:relative; min-width:0; overflow:hidden; }
  #source { flex:0 0 auto; max-width:46%; background:#111; display:flex; align-items:center; justify-content:center; }
  #source video, #source img { display:block; width:100%; height:100%; object-fit:contain; }
  #source .note { color:#bbb; padding:16px; text-align:center; width:240px; font-size:13px; }
  #view { flex:1 1 auto; background:#fff; }
  #view canvas { display:block; }
  .label { position:absolute; top:12px; left:14px; z-index:2; font-size:12px; font-weight:500; padding:3px 12px; border-radius:20px; background:rgba(255,255,255,.9); box-shadow:0 1px 3px rgba(0,0,0,.08); pointer-events:none; }
  #source .label { background:rgba(0,0,0,.55); color:#fff; box-shadow:none; }
  .hint { position:absolute; top:14px; right:14px; z-index:2; font-size:12px; color:var(--muted); pointer-events:none; }
  .caption { position:absolute; left:0; right:0; bottom:14px; z-index:2; text-align:center; font-size:17px; pointer-events:none; padding:0 16px; text-shadow:0 0 10px #fff, 0 0 4px #fff; }
  .caption .bad { color:var(--red); font-weight:500; }
  .caption .ok { color:var(--green-dark); font-weight:500; }
  #viewMsg { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; color:var(--muted); text-align:center; padding:24px; }

  /* Timeline dock */
  #dock { flex:0 0 auto; display:flex; flex-direction:column; }
  .dockhead { display:flex; align-items:center; gap:8px; padding:10px 14px; border-bottom:1px solid var(--line); flex-wrap:wrap; }
  .dockhead h3 { margin:0 6px 0 0; font-size:15px; color:var(--heading); }
  .round { width:34px; height:34px; border-radius:50%; border:1px solid var(--border); background:#fff; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; transition:all .2s; padding:0; }
  .round:hover { border-color:var(--green); color:var(--green-dark); }
  .round svg, .pill svg { width:14px; height:14px; fill:currentColor; }
  #play { width:auto; padding:0 18px; border-radius:20px; background:var(--green); border-color:var(--green); color:#000; font-weight:500; gap:6px; }
  #play:hover { background:#fff; box-shadow:0 0 15px rgba(118,185,0,.5); color:#000; }
  .framebox { display:inline-flex; align-items:center; gap:6px; padding:5px 12px; border:1px solid var(--border); border-radius:20px; color:var(--subtle); font-size:13px; }
  .framebox input { width:46px; border:none; outline:none; text-align:right; font-family:var(--mono); font-size:13px; color:var(--heading); background:transparent; }
  .framebox .t { font-family:var(--mono); color:var(--muted); }
  .grow { flex:1; }
  button.pill { cursor:pointer; transition:all .2s; }
  button.pill:hover { border-color:var(--green); }
  button.pill.on { background:var(--green); border-color:var(--green); color:#000; }
  button.pill:disabled { opacity:.4; cursor:default; }
  input[type=range] { -webkit-appearance:none; appearance:none; background:transparent; width:80px; }
  input[type=range]::-webkit-slider-runnable-track { height:4px; border-radius:2px; background:var(--border); }
  input[type=range]::-webkit-slider-thumb { -webkit-appearance:none; width:13px; height:13px; margin-top:-4.5px; border-radius:50%; background:var(--green); }
  input[type=range]::-moz-range-track { height:4px; background:var(--border); }
  input[type=range]::-moz-range-thumb { width:13px; height:13px; border-radius:50%; background:var(--green); border:none; }
  #nowbar { display:flex; align-items:center; gap:6px; padding:7px 14px; border-bottom:1px solid var(--line); min-height:36px; overflow:hidden; white-space:nowrap; }
  #nowbar .lab { color:var(--muted); font-size:12px; margin-right:2px; }
  .tag { display:inline-block; padding:1px 10px; border-radius:20px; background:var(--red-soft); color:#b42328; font-size:12px; }
  .clean { color:var(--green-dark); font-size:13px; }
  #tlwrap { max-height:26vh; overflow-y:auto; overflow-x:hidden; padding:4px 6px 8px; }
  #timeline { width:100%; display:block; cursor:pointer; }

  /* Right panel */
  #right { min-height:0; display:flex; flex-direction:column; }
  .phead { flex:0 0 auto; display:flex; align-items:center; gap:8px; padding:12px 16px; border-bottom:1px solid var(--line); cursor:pointer; user-select:none; }
  .phead h3 { margin:0; font-size:15px; color:var(--heading); }
  .phead .tri { color:var(--muted); width:10px; font-size:11px; }
  .phead .count { margin-left:auto; }
  .kv { display:grid; grid-template-columns:120px 1fr; gap:6px 12px; padding:12px 16px; border-bottom:1px solid var(--line); font-size:13px; }
  .kv .k { color:var(--muted); }
  .kv .v { color:var(--heading); font-weight:500; }
  .kv .v.bad { color:var(--red); }
  .filters { display:flex; gap:6px; flex-wrap:wrap; padding:10px 16px; border-bottom:1px solid var(--line); }
  .filters .pill { padding:4px 12px; font-size:12px; }
  #issuesBody { flex:1 1 auto; min-height:0; display:flex; flex-direction:column; }
  #issues { flex:1 1 auto; overflow:auto; padding:8px; }
  .issue { position:relative; border:1px solid var(--line); border-radius:12px; padding:10px 12px; margin-bottom:8px; cursor:pointer; transition:all .15s; background:#fff; }
  .issue:hover { box-shadow:0 4px 12px rgba(0,0,0,.07); }
  .issue.sel { border-color:var(--green); box-shadow:0 0 0 2px rgba(118,185,0,.3); background:var(--green-soft); }
  .issue .t { font-weight:700; color:var(--heading); padding-right:70px; }
  .issue .d { position:absolute; top:10px; right:12px; font-weight:700; color:var(--red); }
  .issue.restpose .d { color:var(--muted); }
  .issue .m { color:var(--subtle); font-size:12.5px; margin-top:3px; }
  .issue .r { color:var(--muted); font-size:12px; margin-top:3px; font-family:var(--mono); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .issue .badge { display:inline-block; margin-top:6px; font-size:11px; padding:1px 8px; border-radius:20px; border:1px solid var(--border); color:var(--muted); }
  .empty { padding:18px; text-align:center; color:var(--muted); }
  #method { margin:0; padding:12px 16px 14px 32px; color:var(--subtle); font-size:13px; line-height:1.55; max-height:30vh; overflow:auto; }
  #method li { margin:5px 0; }
  #method b { color:var(--heading); }
  .collapsed + * { display:none !important; }
  ::-webkit-scrollbar { width:10px; height:10px; } ::-webkit-scrollbar-thumb { background:#d6d6d6; border:3px solid #fff; border-radius:6px; } ::-webkit-scrollbar-thumb:hover { background:#bdbdbd; }
  @media (max-width:980px) { body { overflow:auto; height:auto; } #work { grid-template-columns:1fr; } #viewports { height:60vh; } #meta { display:none; } }
</style>
<script type="importmap">{"imports":{"three":"__THREE__/build/three.module.js","three/addons/":"__THREE__/examples/jsm/"}}</script>
</head>
<body>
<div id="titlebar">
  <div class="brand"><span class="mark"></span>Motion2MixamoRig <span class="g">Diagnostics</span></div>
  <div id="meta"></div>
  <span class="pill" id="status"></span>
</div>

<div id="work">
  <div id="left">
    <div class="card" id="viewports">
      <div class="vp" id="source"><span class="label" id="srcLabel">Original</span></div>
      <div class="vp" id="view">
        <span class="label">Character</span>
        <span class="hint">Drag to orbit · scroll to zoom</span>
        <div class="caption" id="caption"></div>
        <div id="viewMsg">Loading the 3D view…</div>
      </div>
    </div>

    <div class="card" id="dock">
      <div class="dockhead">
        <h3>Timeline</h3>
        <button class="round" id="first" title="First frame"><svg viewBox="0 0 16 16"><path d="M3 2h2v12H3zM13 2v12L6 8z"/></svg></button>
        <button class="round" id="prev" title="Previous frame (←)"><svg viewBox="0 0 16 16"><path d="M11 2v12L4 8z"/></svg></button>
        <button class="round" id="play" title="Play / Pause (Space)"></button>
        <button class="round" id="next" title="Next frame (→)"><svg viewBox="0 0 16 16"><path d="M5 2v12l7-6z"/></svg></button>
        <button class="round" id="last" title="Last frame"><svg viewBox="0 0 16 16"><path d="M11 2h2v12h-2zM3 2v12l7-6z"/></svg></button>
        <span class="framebox">Frame <input id="frameField" inputmode="numeric" title="Type a frame and press Enter"> <span id="frameTotal"></span> <span class="t" id="timeInfo"></span></span>
        <div class="grow"></div>
        <button class="pill" id="sound" title="Sound of the original video"></button>
        <input id="volume" type="range" min="0" max="1" step="0.05" value="0.8" title="Volume">
      </div>
      <div id="nowbar"><span class="lab">At this frame</span><span id="now"></span></div>
      <div id="tlwrap"><canvas id="timeline"></canvas></div>
    </div>
  </div>

  <div class="card" id="right">
    <div class="phead" data-toggle><span class="tri">▾</span><h3>Summary</h3></div>
    <div class="kv" id="summary"></div>
    <div class="phead" data-toggle><span class="tri">▾</span><h3>Issues</h3><span class="pill count" id="issueCount"></span></div>
    <div id="issuesBody">
      <div class="filters" id="filters">
        <button class="pill on" data-f="all">All pairs</button>
        <button class="pill" data-f="motion">Only from motion</button>
        <button class="pill" data-f="now">On this frame</button>
      </div>
      <div id="issues"></div>
    </div>
    <div class="phead collapsed" data-toggle><span class="tri">▸</span><h3>Method</h3></div>
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
  play: '<svg viewBox="0 0 16 16"><path d="M4 2l10 6-10 6z"/></svg> Play',
  pause: '<svg viewBox="0 0 16 16"><path d="M3 2h4v12H3zM9 2h4v12H9z"/></svg> Pause',
  on: '<svg viewBox="0 0 16 16"><path d="M2 6h3l4-3v10l-4-3H2zM11 5.5a3.5 3.5 0 010 5l-.8-.8a2.4 2.4 0 000-3.4zM12.6 3.9a5.8 5.8 0 010 8.2l-.8-.8a4.7 4.7 0 000-6.6z"/></svg> Sound on',
  off: '<svg viewBox="0 0 16 16"><path d="M2 6h3l4-3v10l-4-3H2zM11 6.2l.8-.8 1.6 1.6 1.6-1.6.8.8L14.2 8l1.6 1.6-.8.8-1.6-1.6-1.6 1.6-.8-.8L12.6 8z"/></svg> Sound off',
};

// Collapsible panels.
document.querySelectorAll('[data-toggle]').forEach(h => h.onclick = () => {
  h.classList.toggle('collapsed'); h.querySelector('.tri').textContent = h.classList.contains('collapsed') ? '▸' : '▾';
  setTimeout(drawTimeline, 0);
});

// Original video / photo, on the same timeline (frame k at k / fps).
const M = D.media, src = $('source');
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
  src.append(el);
  $('srcLabel').textContent = 'Original · ' + M.name;
} else {
  src.style.width = '260px';
  const n = document.createElement('div'); n.className = 'note'; n.textContent = M.note || 'No source video.'; src.append(n);
}

// Sound: off by default (browsers block autoplay with sound); one click turns it on.
function showSound() { $('sound').innerHTML = video && !video.muted ? ICON.on : ICON.off; $('sound').classList.toggle('on', !!video && !video.muted); }
if (video) {
  video.volume = +$('volume').value;
  $('sound').onclick = () => { video.muted = !video.muted; showSound(); };
  $('volume').oninput = e => { video.volume = +e.target.value; if (video.muted && video.volume > 0) { video.muted = false; showSound(); } };
} else { $('sound').disabled = true; $('volume').disabled = true; }
showSound();

// Title bar and summary.
const S = R.summary.self_intersection;
const pill = (k, v, cls = '') => `<span class="pill ${cls}"><span class="k">${k}</span> ${v}</span>`;
$('meta').innerHTML = [pill('Source', R.source), pill('Frames', `${N} @ ${FPS} fps`), pill('Threshold', `${R.threshold_cm} cm`)].join('');
$('status').className = 'pill ' + (S.issue_count ? 'alert' : 'solid');
$('status').textContent = S.issue_count ? `${S.issue_count} self-intersections · deepest ${S.max_depth_cm} cm` : 'No self-intersection';
const kv = [
  ['Check', 'Self-intersection'],
  ['Part pairs', S.issue_count, S.issue_count > 0],
  ['Frames affected', `${S.frame_count} / ${N} (${(100 * S.frame_count / Math.max(1, N)).toFixed(1)}%)`, S.frame_count > 0],
  ['Deepest', `${S.max_depth_cm} cm`, S.max_depth_cm > 0],
  ['Frame numbers', 'Blender frames (first = 0)'],
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
    el.querySelector('.r').textContent = 'Frames ' + i.ranges.map(fmtRange).join(', ');
    if (i.also_in_rest_pose) { const b = document.createElement('span'); b.className = 'badge'; b.textContent = 'Also in rest pose'; el.append(b); }
    el.onclick = () => { stop(); selected = idx; setFrame(i.worst_frame); renderList(); };
    box.append(el);
  });
}
document.querySelectorAll('#filters .pill').forEach(b => b.onclick = () => {
  filter = b.dataset.f; document.querySelectorAll('#filters .pill').forEach(x => x.classList.toggle('on', x === b)); renderList(); drawTimeline();
});

// Timeline: label column, ruler, one track per issue, green playhead.
const TL = { label: 180, ruler: 24, row: 20, pad: 12 };
function drawTimeline() {
  const c = $('timeline'), items = filter === 'now' ? R.issues : visible();
  const w = c.clientWidth || c.parentElement.clientWidth, h = TL.ruler + Math.max(1, items.length) * TL.row + 4;
  const dpr = window.devicePixelRatio || 1;
  c.width = w * dpr; c.height = h * dpr; c.style.height = h + 'px';
  const g = c.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
  const x0 = TL.label + TL.pad, x1 = w - TL.pad, x = f => x0 + (x1 - x0) * (N > 1 ? f / (N - 1) : 0);
  g.clearRect(0, 0, w, h);
  const font = '"Google Sans", "Segoe UI", system-ui, sans-serif';
  const pxPerFrame = (x1 - x0) / Math.max(1, N - 1);
  const major = [1, 5, 10, 25, 50, 100, 250, 500, 1000].find(s => s * pxPerFrame >= 60) || 1000;
  const minor = major >= 10 ? major / 5 : 1;
  g.font = `11px ${font}`; g.textBaseline = 'top'; g.textAlign = 'center';
  for (let f = 0; f < N; f += minor) {
    const isMajor = f % major === 0, xx = Math.round(x(f)) + .5;
    g.strokeStyle = isMajor ? '#bbb' : '#e2e2e2'; g.beginPath(); g.moveTo(xx, TL.ruler - (isMajor ? 8 : 4)); g.lineTo(xx, TL.ruler - 1); g.stroke();
    if (isMajor) { g.fillStyle = '#8a8a8a'; g.fillText(String(f), xx, 2); }
  }
  g.textAlign = 'left';
  items.forEach((i, k) => {
    const y = TL.ruler + k * TL.row, idx = R.issues.indexOf(i), sel = idx === selected;
    g.fillStyle = sel ? '#f1f8e4' : (k % 2 ? '#fafafa' : '#ffffff'); g.fillRect(0, y, w, TL.row);
    g.fillStyle = sel ? '#4a7a00' : (i.also_in_rest_pose ? '#9a9a9a' : '#333'); g.textBaseline = 'middle';
    g.font = `${sel ? 700 : 400} 12.5px ${font}`;
    let name = pairName(i); while (g.measureText(name).width > TL.label - 10 && name.length > 4) name = name.slice(0, -2) + '…';
    g.fillText(name, 8, y + TL.row / 2 + .5);
    g.fillStyle = '#efefef'; g.fillRect(x0, y + TL.row / 2 - 1, x1 - x0, 2);
    g.fillStyle = i.also_in_rest_pose ? '#c4c4c4' : '#e5484d';
    for (const [a, b] of i.ranges) { g.beginPath(); g.roundRect(x(a) - 1, y + 5, Math.max(3, x(b) - x(a) + 2), TL.row - 10, 3); g.fill(); }
  });
  const px = Math.round(x(frame)) + .5;
  g.strokeStyle = '#76b900'; g.lineWidth = 2; g.beginPath(); g.moveTo(px, TL.ruler - 2); g.lineTo(px, h); g.stroke(); g.lineWidth = 1;
  g.fillStyle = '#76b900'; g.beginPath(); g.roundRect(px - 16, 0, 32, 16, 8); g.fill();
  g.fillStyle = '#000'; g.font = `500 11px ${font}`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(String(frame), px, 8.5); g.textAlign = 'left';

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
const view = document.getElementById('view'), msg = document.getElementById('viewMsg');
const bytes = Uint8Array.from(atob(document.getElementById('glb').textContent.trim()), c => c.charCodeAt(0));

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(window.devicePixelRatio || 1);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
view.prepend(renderer.domElement);

// Light studio: white tiled floor fading into a white horizon, soft contact shadow.
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);
scene.fog = new THREE.Fog(0xffffff, 5, 16);
const camera = new THREE.PerspectiveCamera(35, 1, 0.01, 100);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
scene.add(new THREE.HemisphereLight(0xffffff, 0xdfe3ea, 1.9));
const sun = new THREE.DirectionalLight(0xffffff, 1.6);
sun.position.set(2.5, 6, 3); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048); sun.shadow.radius = 6;
Object.assign(sun.shadow.camera, { left: -2, right: 2, top: 2, bottom: -2, near: 0.5, far: 20 });
scene.add(sun); scene.add(sun.target);
const tile = document.createElement('canvas'); tile.width = tile.height = 256;
const tg = tile.getContext('2d'); tg.fillStyle = '#ffffff'; tg.fillRect(0, 0, 256, 256);
tg.strokeStyle = '#d4d4d4'; tg.lineWidth = 3; tg.strokeRect(0, 0, 256, 256);
const tex = new THREE.CanvasTexture(tile);
tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(80, 80); tex.colorSpace = THREE.SRGBColorSpace;
tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
const ground = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshStandardMaterial({ map: tex, roughness: 1, metalness: 0 }));
ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);

function size() { const w = view.clientWidth, h = view.clientHeight; renderer.setSize(w, h); camera.aspect = w / Math.max(1, h); camera.updateProjectionMatrix(); }
window.addEventListener('resize', size); size();

const BASE = new THREE.Color(0x93a6e6), HOT = new THREE.Color(0xe5484d);
new GLTFLoader().parse(bytes.buffer, '', gltf => {
  msg.remove();
  scene.add(gltf.scene);
  const mixer = new THREE.AnimationMixer(gltf.scene);
  if (gltf.animations[0]) mixer.clipAction(gltf.animations[0]).play();

  // Matte periwinkle character; parts in an issue on this frame turn red.
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
    o.material = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.85, metalness: 0 });
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
  ground.position.y = box.min.y;
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
