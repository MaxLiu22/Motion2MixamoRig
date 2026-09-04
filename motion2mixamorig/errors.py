"""Map pipeline exceptions to a short code + one-line message.

Tracebacks stay on stderr / the job log. JSONL and `run.json` only get the
short message.
"""

from __future__ import annotations


def classify_error(exc: BaseException) -> tuple[str, str]:
    """Return `(error_code, human_message)` for a caught pipeline exception."""
    text = str(exc).strip()
    low = text.lower()
    name = type(exc).__name__

    if isinstance(exc, ModuleNotFoundError) or "no module named" in low:
        return "PACKAGE_MISSING", "Motion2MixamoRig package not installed"

    if isinstance(exc, FileNotFoundError):
        if "smplx" in low or "smpl" in low:
            return "SMPLX_MISSING", "SMPL-X model missing"
        return "FILE_NOT_FOUND", _short_message(text) or "A required file was not found"

    if _looks_like_cuda(low):
        return "CUDA_UNAVAILABLE", "CUDA unavailable"

    if "mps" in low and ("not available" in low or "not built" in low or "not supported" in low):
        return "MPS_UNAVAILABLE", "Apple MPS unavailable"

    if "people" in low and ("in frame" in low or "shows about" in low or "group" in low):
        return "MULTIPLE_PEOPLE", "Input contains multiple people"

    if "no person" in low:
        return "NO_PERSON", "No person was detected in the input"

    if "mixamo" in low or "fbx" in low:
        return "INVALID_RIG", "Mixamo FBX invalid"

    if "smplx" in low or "smpl-x" in low or "smpl_x" in low:
        return "SMPLX_MISSING", "SMPL-X model missing"

    if name == "ValueError" and "video or an image" in low:
        return "INVALID_INPUT", "A video or image is required"

    return "PIPELINE_FAILED", _short_message(text) or "Pipeline failed"


def _looks_like_cuda(low: str) -> bool:
    if "cuda" not in low:
        return False
    hints = (
        "not available",
        "not compiled",
        "no kernel image",
        "cudaerror",
        "invalid device",
        "out of memory",
        "no cuda gpus",
    )
    return any(hint in low for hint in hints)


def _short_message(text: str, limit: int = 160) -> str:
    if not text:
        return ""
    first = text.splitlines()[0].strip()
    if len(first) > limit:
        return first[: limit - 1] + "…"
    return first
