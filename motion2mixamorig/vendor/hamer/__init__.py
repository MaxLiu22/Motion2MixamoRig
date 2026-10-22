"""Minimal HaMeR (Pavlakos et al., CVPR 2024) inference code, vendored.

Copied from https://github.com/geopavlakos/hamer (MIT, see LICENSE.md):
the ViT-H backbone, the MANO transformer head, the MANO joint wrapper and
the hand-crop helpers. Training, datasets, renderers, detectron2 and mmpose
are left out; hand boxes come from the body extractor's wrist keypoints.
"""
