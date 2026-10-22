"""HaMeR MANO transformer-decoder head (hamer/models/heads/mano_head.py), without yacs.

The constants are the released hamer.ckpt configuration (model_config.yaml):
6d joint representation, 15 hand joints + global orient, zero input token,
one IEF iteration, decoder depth 6 / heads 8 / mlp 1024 / context 1280.
"""

from __future__ import annotations

import einops
import numpy as np
import torch
import torch.nn as nn

from .geometry import rot6d_to_rotmat
from .pose_transformer import TransformerDecoder

NUM_HAND_JOINTS = 15


class MANOTransformerDecoderHead(nn.Module):
    """Cross-attention based MANO Transformer decoder."""

    def __init__(self, mean_params_npz: str):
        super().__init__()
        self.joint_rep_dim = 6
        self.npose = self.joint_rep_dim * (NUM_HAND_JOINTS + 1)
        self.transformer = TransformerDecoder(
            num_tokens=1,
            token_dim=1,
            dim=1024,
            depth=6,
            heads=8,
            mlp_dim=1024,
            dim_head=64,
            dropout=0.0,
            emb_dropout=0.0,
            norm="layer",
            context_dim=1280,
        )
        dim = 1024
        self.decpose = nn.Linear(dim, self.npose)
        self.decshape = nn.Linear(dim, 10)
        self.deccam = nn.Linear(dim, 3)

        mean_params = np.load(mean_params_npz)
        self.register_buffer("init_hand_pose", torch.from_numpy(mean_params["pose"].astype(np.float32)).unsqueeze(0))
        self.register_buffer("init_betas", torch.from_numpy(mean_params["shape"].astype(np.float32)).unsqueeze(0))
        self.register_buffer("init_cam", torch.from_numpy(mean_params["cam"].astype(np.float32)).unsqueeze(0))

    def forward(self, x: torch.Tensor):
        batch_size = x.shape[0]
        x = einops.rearrange(x, "b c h w -> b (h w) c")  # channel-first -> token-first
        token = torch.zeros(batch_size, 1, 1, device=x.device, dtype=x.dtype)
        token_out = self.transformer(token, context=x).squeeze(1)
        pred_hand_pose = self.decpose(token_out) + self.init_hand_pose.expand(batch_size, -1)
        pred_betas = self.decshape(token_out) + self.init_betas.expand(batch_size, -1)
        pred_cam = self.deccam(token_out) + self.init_cam.expand(batch_size, -1)
        rotmats = rot6d_to_rotmat(pred_hand_pose).view(batch_size, NUM_HAND_JOINTS + 1, 3, 3)
        return {"global_orient": rotmats[:, 0], "hand_pose": rotmats[:, 1:], "betas": pred_betas}, pred_cam
