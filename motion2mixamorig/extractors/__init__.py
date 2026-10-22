"""Motion extractors. Each one reads a video or a still and writes skeleton_motion.npz."""

from __future__ import annotations

from .base import MotionExtractor
from .gvhmr import GvhmrExtractor

DEFAULT_EXTRACTOR = "gvhmr"

_EXTRACTORS: dict[str, MotionExtractor] = {
    GvhmrExtractor.name: GvhmrExtractor(),
}


def extractor_names() -> tuple[str, ...]:
    return tuple(_EXTRACTORS)


def get_extractor(name: str) -> MotionExtractor:
    try:
        return _EXTRACTORS[name]
    except KeyError as exc:
        choices = ", ".join(extractor_names())
        raise ValueError(f"unknown extractor {name!r}; choose from {choices}") from exc
