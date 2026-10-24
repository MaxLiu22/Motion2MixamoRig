#!/usr/bin/env python3
"""Build the Motion2MixamoRig add-on zip for Blender 4.2+.

Release builds are per platform:

    python scripts/package_blender_extension.py --platform macos-arm64
    -> dist/motion2mixamorig-<version>-macos-arm64.zip

The platform goes into the zip name and into `platforms` in the zip's
blender_manifest.toml, so Blender refuses to install it on another OS. The
version stays the same on every platform. Pass --platform more than once to
build several zips. Without --platform you get a platform-neutral
dist/motion2mixamorig-<version>.zip for local testing only.

The zip root contains blender_manifest.toml and __init__.py directly — no
extra wrapping folder.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "blender_extension" / "motion2mixamorig_blender"
DIST = ROOT / "dist"
REQUIRED_MANIFEST_FIELDS = (
    "schema_version",
    "id",
    "version",
    "name",
    "tagline",
    "maintainer",
    "type",
    "blender_version_min",
    "license",
)
SKIP_NAMES = {".DS_Store", ".gitkeep"}
# Motion2MixamoRig itself rides inside the zip under backend/, so the one-click
# runtime setup installs exactly the code that matches this add-on version.
BACKEND_ITEMS = ("motion2mixamorig", "pyproject.toml", "LICENSE", "NOTICE.md")
# Platform names Blender accepts in the manifest `platforms` field.
PLATFORMS = ("macos-arm64", "macos-x64", "windows-x64", "windows-arm64", "linux-x64")


def read_manifest(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("["):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def extension_version(src: Path = SRC) -> str:
    manifest = read_manifest(src / "blender_manifest.toml")
    return manifest.get("version", "0.1.8")


def should_include(path: Path) -> bool:
    if path.name in SKIP_NAMES or path.suffix == ".pyc":
        return False
    return not any(part == "__pycache__" for part in path.parts)


def iter_source_files(src: Path) -> list[Path]:
    return sorted(p for p in src.rglob("*") if p.is_file() and should_include(p))


def manifest_for_platform(text: str, platform: str) -> str:
    """Set top-level `platforms` (before the first [table], as TOML requires)."""
    lines = [line for line in text.splitlines() if not line.strip().startswith("platforms")]
    entry = f'platforms = ["{platform}"]'
    for i, line in enumerate(lines):
        if line.strip().startswith("["):
            lines[i:i] = [entry, ""]
            break
    else:
        lines.append(entry)
    return "\n".join(lines) + "\n"


def build_zip(src: Path = SRC, dest: Path | None = None, platform: str | None = None) -> Path:
    if not (src / "blender_manifest.toml").is_file() or not (src / "__init__.py").is_file():
        raise FileNotFoundError(f"extension sources are incomplete: {src}")
    if platform is not None and platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}; expected one of {', '.join(PLATFORMS)}")
    version = extension_version(src)
    suffix = f"-{platform}" if platform else ""
    dest = dest or (DIST / f"motion2mixamorig-{version}{suffix}.zip")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in iter_source_files(src):
            arcname = path.relative_to(src).as_posix()
            if platform and arcname == "blender_manifest.toml":
                text = path.read_text(encoding="utf-8")
                archive.writestr(arcname, manifest_for_platform(text, platform))
                continue
            archive.write(path, arcname)
        for name in BACKEND_ITEMS:
            item = ROOT / name
            files = iter_source_files(item) if item.is_dir() else [item]
            for path in files:
                archive.write(path, ("backend" / path.relative_to(ROOT)).as_posix())
    errors = validate_zip(dest, platform)
    if errors:
        raise RuntimeError("invalid extension zip:\n" + "\n".join(errors))
    return dest


def validate_zip(zip_path: Path, platform: str | None = None) -> list[str]:
    errors: list[str] = []
    if not zip_path.is_file():
        return [f"zip does not exist: {zip_path}"]
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    if "blender_manifest.toml" not in names:
        errors.append("zip root is missing blender_manifest.toml")
    if "__init__.py" not in names:
        errors.append("zip root is missing __init__.py")
    if "backend/motion2mixamorig/cli.py" not in names:
        errors.append("zip is missing the bundled backend (backend/motion2mixamorig)")
    if any(name.startswith("motion2mixamorig_blender/") for name in names):
        errors.append("zip has an extra wrapping directory")
    if any(name.startswith("blender_extension/") for name in names):
        errors.append("zip includes the repository blender_extension/ prefix")
    top_dirs = {name.split("/", 1)[0] for name in names if "/" in name}
    if "blender_manifest.toml" in names and "motion2mixamorig_blender" in top_dirs:
        errors.append("zip root is nested under motion2mixamorig_blender/")
    try:
        with zipfile.ZipFile(zip_path) as archive:
            manifest_text = archive.read("blender_manifest.toml").decode("utf-8")
    except KeyError:
        return errors
    for field in REQUIRED_MANIFEST_FIELDS:
        if f"{field} =" not in manifest_text and f"{field}=" not in manifest_text:
            errors.append(f"manifest is missing {field}")
    if 'id = "motion2mixamorig"' not in manifest_text:
        errors.append("manifest id must be motion2mixamorig")
    if platform and f'platforms = ["{platform}"]' not in manifest_text:
        errors.append(f"manifest does not declare platforms = [\"{platform}\"]")
    return errors


def maybe_blender_validate(zip_path: Path) -> str | None:
    blender = shutil.which("blender")
    candidates = [
        Path(blender) if blender else None,
        Path("/Applications/Blender.app/Contents/MacOS/Blender"),
        Path(r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"),
        Path(r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"),
    ]
    binary = next((path for path in candidates if path is not None and path.is_file()), None)
    if binary is None:
        return None
    import subprocess

    completed = subprocess.run(
        [str(binary), "--command", "extension", "validate", str(zip_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    if completed.returncode != 0:
        raise RuntimeError(f"blender extension validate failed:\n{output}")
    return output.strip() or "blender extension validate: ok"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the Motion2MixamoRig add-on zip (one per --platform for releases).",
    )
    parser.add_argument("--output", type=Path, default=None, help="zip path (only with zero or one --platform)")
    parser.add_argument(
        "--platform",
        action="append",
        choices=PLATFORMS,
        default=None,
        help="target platform; repeat for several zips. Omit for a platform-neutral test build.",
    )
    args = parser.parse_args(argv)
    platforms = args.platform or [None]
    if args.output is not None and len(platforms) > 1:
        parser.error("--output works with at most one --platform")
    for platform in platforms:
        dest = build_zip(dest=args.output, platform=platform)
        print(f"wrote {dest}")
        try:
            message = maybe_blender_validate(dest)
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            return 1
        if message:
            print(message)
        else:
            print("Blender CLI not found; zip structure and manifest were checked locally.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
