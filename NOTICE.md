# NOTICE

This project's own code is released under the license in `LICENSE`. It builds
on the following upstream components, each governed by its own terms. None of
their gated assets are redistributed here; users obtain them directly from the
sources below.

## GVHMR

World-Grounded Human Motion Recovery via Gravity-View Coordinates
(Shen et al., SIGGRAPH Asia 2024). Installed as the `gvhmr` Python package.
GVHMR is released for **non-commercial research purposes only** — see its
license before any commercial use.
https://github.com/zju3dv/GVHMR

## SMPL-X body model

The SMPL-X body model is registration-gated and licensed by the Max Planck
Institute for Intelligent Systems for non-commercial scientific research.
Users must register and download `SMPLX_NEUTRAL.npz` themselves.
https://smpl-x.is.tue.mpg.de/

## Adobe Mixamo characters

Mixamo characters (Y Bot and others) are provided by Adobe under the Mixamo
terms of use. Download them with your own Adobe account; the FBX files are
never committed to this repository.
https://www.mixamo.com/

## Inference weights

The extraction step auto-downloads model checkpoints (GVHMR, HMR2, RTMPose /
ViTPose 2D pose, YOLOv8 person detector) into `weights/`. Note that YOLOv8
(Ultralytics) is licensed under **AGPL-3.0**, and the pose/HMR checkpoints
carry their respective research licenses.

## Summary

The end-to-end pipeline is effectively restricted to non-commercial /
research use by its upstream components, regardless of this repository's own
code license.
