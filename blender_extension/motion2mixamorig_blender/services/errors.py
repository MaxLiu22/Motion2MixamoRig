"""Turn process logs and exceptions into short UI messages."""

from __future__ import annotations


ERROR_MESSAGES = {
    "PYTHON_NOT_FOUND": "External Python not found",
    "PACKAGE_MISSING": "Motion2MixamoRig package not installed",
    "SMPLX_MISSING": "SMPL-X model missing",
    "INVALID_RIG": "Mixamo FBX invalid",
    "MULTIPLE_PEOPLE": "Input contains multiple people",
    "NO_PERSON": "No person was detected in the input",
    "CUDA_UNAVAILABLE": "CUDA unavailable",
    "MPS_UNAVAILABLE": "Apple MPS unavailable",
    "PROCESS_EXITED": "Pipeline process exited unexpectedly",
    "GLB_MISSING": "Result GLB not found",
    "JSON_INVALID": "Result JSON is invalid",
    "PREFLIGHT_FAILED": "Input check failed",
    "PIPELINE_FAILED": "Motion2MixamoRig pipeline failed",
}

_CODE_TO_KEY = {
    "PYTHON_NOT_FOUND": "err_python",
    "PACKAGE_MISSING": "err_package",
    "SMPLX_MISSING": "err_smplx",
    "INVALID_RIG": "err_invalid_rig",
    "MULTIPLE_PEOPLE": "err_multiple_people",
    "NO_PERSON": "err_no_person",
    "CUDA_UNAVAILABLE": "err_cuda",
    "MPS_UNAVAILABLE": "err_mps",
    "PROCESS_EXITED": "err_process_exited",
    "GLB_MISSING": "err_glb",
    "JSON_INVALID": "err_json",
    "PREFLIGHT_FAILED": "err_preflight",
    "PIPELINE_FAILED": "err_pipeline",
}


def key_for_code(code: str) -> str:
    return _CODE_TO_KEY.get(code, "err_pipeline")


def message_for_code(code: str, fallback: str = "") -> str:
    return ERROR_MESSAGES.get(code, fallback or ERROR_MESSAGES["PIPELINE_FAILED"])


def classify_log_text(text: str) -> tuple[str, str]:
    """Guess an error code from captured stdout/stderr."""
    low = (text or "").lower()
    if not low.strip():
        return "PROCESS_EXITED", message_for_code("PROCESS_EXITED")

    if "no module named 'motion2mixamorig'" in low or "no module named motion2mixamorig" in low:
        return "PACKAGE_MISSING", message_for_code("PACKAGE_MISSING")
    if "no module named 'torch'" in low or "no module named 'gvhmr'" in low:
        return "PACKAGE_MISSING", message_for_code("PACKAGE_MISSING")
    if "smplx" in low and (
        "missing" in low or "not found" in low or "[missing]" in low or "filenotfound" in low
    ):
        return "SMPLX_MISSING", message_for_code("SMPLX_MISSING")
    if "people in frame" in low or ("shows about" in low and "people" in low):
        return "MULTIPLE_PEOPLE", message_for_code("MULTIPLE_PEOPLE")
    if "no person was detected" in low:
        return "NO_PERSON", message_for_code("NO_PERSON")
    if "cuda" in low and (
        "not available" in low
        or "not compiled" in low
        or "no cuda gpus" in low
        or "cudaerror" in low
    ):
        return "CUDA_UNAVAILABLE", message_for_code("CUDA_UNAVAILABLE")
    if "mps" in low and ("not available" in low or "not built" in low):
        return "MPS_UNAVAILABLE", message_for_code("MPS_UNAVAILABLE")
    if "is not a *binary* fbx" in low or "has no mixamo skeleton" in low:
        return "INVALID_RIG", message_for_code("INVALID_RIG")
    if "could not be parsed as an fbx" in low:
        return "INVALID_RIG", message_for_code("INVALID_RIG")
    if "result json is invalid" in low or "jsondecodeerror" in low:
        return "JSON_INVALID", message_for_code("JSON_INVALID")
    if "mixamo_character.glb" in low and ("not found" in low or "missing" in low):
        return "GLB_MISSING", message_for_code("GLB_MISSING")
    if "input check failed" in low or "problem(s) — nothing was run" in low:
        return "PREFLIGHT_FAILED", message_for_code("PREFLIGHT_FAILED")
    return "PIPELINE_FAILED", message_for_code("PIPELINE_FAILED")
