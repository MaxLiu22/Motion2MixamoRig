"""Human skeleton -> Mixamo rig retargeting.

Modules:
    fbx_skeleton       binary FBX parser, core-bone skeleton extraction
    kinematics         FK with FBX PreRotation, rotation utilities
    retarget           per-frame Human -> Mixamo Skeleton swing/aim retarget
    tpose_calibration  measured T-pose alignment skeleton <-> character rig
    ybot_retarget      rest-relative rotation transfer onto the full rig
    skinned_mesh       FBX meshes, skin clusters, linear blend skinning
    animation          whole-clip retargeting driver
    render             software cameras, skeleton/mesh drawing, video writing
"""
