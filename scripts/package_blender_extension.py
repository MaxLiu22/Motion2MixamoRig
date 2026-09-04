#!/usr/bin/env python3
"""Build dist/motion2mixamorig-0.1.0.zip for Blender 4.2+.

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
    return manifest.get("version", "0.1.0")


def should_include(path: Path) -> bool:
    if path.name in SKIP_NAMES or path.suffix == ".pyc":
        return False
    return not any(part == "__pycache__" for part in path.parts)


def iter_source_files(src: Path) -> list[Path]:
    return sorted(p for p in src.rglob("*") if p.is_file() and should_include(p))


def build_zip(src: Path = SRC, dest: Path | None = None) -> Path:
    if not (src / "blender_manifest.toml").is_file() or not (src / "__init__.py").is_file():
        raise FileNotFoundError(f"extension sources are incomplete: {src}")
    version = extension_version(src)
    dest = dest or (DIST / f"motion2mixamorig-{version}.zip")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in iter_source_files(src):
            archive.write(path, path.relative_to(src).as_posix())
    errors = validate_zip(dest)
    if errors:
        raise RuntimeError("invalid extension zip:\n" + "\n".join(errors))
    return dest


def validate_zip(zip_path: Path) -> list[str]:
    errors: list[str] = []
    if not zip_path.is_file():
        return [f"zip does not exist: {zip_path}"]
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    if "blender_manifest.toml" not in names:
        errors.append("zip root is missing blender_manifest.toml")
    if "__init__.py" not in names:
        errors.append("zip root is missing __init__.py")
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None, help="zip path")
    args = parser.parse_args(argv)
    dest = build_zip(dest=args.output)
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
