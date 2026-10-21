"""Subject-selection regressions. Run: python -m unittest discover -s scripts -p 'test_*.py'."""

from pathlib import Path
import argparse
import contextlib
import io
import json
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from motion2mixamorig import checks
from motion2mixamorig.cli import build_parser, preflight
from motion2mixamorig.person_selection import (
    PersonSelectionError, collect_tracks, interpolate_track, selected_track, source_key,
)


class SubjectSelectionTests(unittest.TestCase):
    def test_select_smaller_person_when_detections_change_order(self):
        history = [
            [{"id": 1, "bbx_xyxy": [0, 0, 100, 100]}, {"id": 2, "bbx_xyxy": [120, 0, 150, 40]}],
            [{"id": 2, "bbx_xyxy": [125, 0, 155, 40]}, {"id": 1, "bbx_xyxy": [5, 0, 105, 100]}],
        ]
        data = {"tracks": collect_tracks(history)}
        boxes, observed = interpolate_track(selected_track(data, 2), 2)
        np.testing.assert_allclose(boxes[:, 0], [120, 125])
        self.assertTrue(observed.all())

    def test_short_gap_is_interpolated_and_marked_unobserved(self):
        track = {"id": 7, "frames": [0, 2], "boxes": [[0, 0, 10, 20], [10, 0, 20, 20]]}
        boxes, observed = interpolate_track(track, 3)
        np.testing.assert_allclose(boxes[1], [5, 0, 15, 20])
        self.assertEqual(observed.tolist(), [True, False, True])

    def test_long_gap_does_not_follow_a_different_identity(self):
        history = [[{"id": 1, "bbx_xyxy": [0, 0, 10, 20]}]]
        history += [[{"id": 2, "bbx_xyxy": [0, 0, 10, 20]}] for _ in range(17)]
        track = selected_track({"tracks": collect_tracks(history)}, 1)
        with self.assertRaisesRegex(PersonSelectionError, "untracked for 17 frames"):
            interpolate_track(track, 18)

    def test_invalid_id_lists_choices(self):
        with self.assertRaisesRegex(PersonSelectionError, "Available IDs: 2, 8"):
            selected_track({"tracks": [{"id": 2}, {"id": 8}]}, 1)

    def test_replaced_source_gets_a_new_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "video.mp4"
            source.write_bytes(b"first")
            key = source_key(source)
            source.write_bytes(b"replacement")
            self.assertNotEqual(key, source_key(source))

    def test_bad_box_and_out_of_order_frames_are_rejected(self):
        for frames, boxes in [([1, 0], [[0, 0, 1, 1]] * 2), ([0], [[5, 0, 1, 1]])]:
            with self.subTest(frames=frames, boxes=boxes):
                with self.assertRaises(PersonSelectionError):
                    interpolate_track({"id": 1, "frames": frames, "boxes": boxes}, 2)

    def test_group_image_requires_selection_by_default(self):
        import cv2

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "group.jpg"
            cv2.imwrite(str(source), np.zeros((32, 64, 3), dtype=np.uint8))
            with patch.object(checks, "_count_people", return_value=2) as count:
                self.assertIn("--select-person", checks.check_image(source))
                count.reset_mock()
                self.assertIsNone(checks.check_image(source, check_people=False))
                count.assert_not_called()

    def test_selection_still_rejects_undecodable_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "broken.jpg"
            source.write_text("not a picture")
            self.assertIsNotNone(checks.check_image(source, check_people=False))

    def test_cli_selection_flags_are_exclusive(self):
        parser = build_parser()
        self.assertEqual(parser.parse_args(["run", "--person", "2"]).person, 2)
        with self.assertRaises(SystemExit):
            parser.parse_args(["run", "--person", "2", "--select-person"])
        with self.assertRaises(SystemExit):
            parser.parse_args(["run", "--person", "0"])

    def test_reused_skeleton_does_not_reject_group_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "group.mp4"
            rig = Path(tmp) / "rig.fbx"
            skeleton = Path(tmp) / "motion.npz"
            for path in (source, rig, skeleton):
                path.touch()
            args = argparse.Namespace(video=str(source), image=None, rig=str(rig),
                                      skeleton=str(skeleton), person=None, select_person=False)
            with patch.object(checks, "check_video", return_value=None) as video_check, \
                 patch.object(checks, "check_rig", return_value=None), \
                 patch.object(checks, "check_skeleton_npz", return_value=None), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(preflight(args)[2], skeleton)
                video_check.assert_called_once_with(source, check_people=False)

    def test_selected_subject_is_written_to_gvhmr_cache(self):
        import cv2
        import torch
        from types import SimpleNamespace
        from motion2mixamorig.person_selection import seed_person_cache

        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            video = folder / "two.mp4"
            writer = cv2.VideoWriter(str(video), cv2.VideoWriter_fourcc(*"mp4v"), 30, (64, 32))
            for _ in range(4):
                writer.write(np.zeros((32, 64, 3), dtype=np.uint8))
            writer.release()
            data = {"source_key": "revision1", "directory": str(folder), "n_frames": 4,
                    "width": 64, "height": 32, "tracks": [
                        {"id": 1, "frames": [0, 1, 2, 3], "boxes": [[0, 0, 30, 32]] * 4},
                        {"id": 2, "frames": [0, 1, 2, 3], "boxes": [[40, 0, 60, 32]] * 4},
                    ]}
            for person_id in (1, 2):
                out = folder / f"person-{person_id}"
                out.mkdir()
                cfg = SimpleNamespace(video_path=video, paths=SimpleNamespace(bbx=out / "bbx.pt"))
                with patch("motion2mixamorig.person_selection.stage_video", return_value=cfg):
                    seed_person_cache(video, out, data, person_id)
                boxes = torch.load(out / "bbx.pt", weights_only=False)["bbx_xyxy"].numpy()
                np.testing.assert_allclose(boxes, data["tracks"][person_id-1]["boxes"])
                self.assertEqual(json.loads((out / "person_selection.json").read_text())["person_id"], person_id)


if __name__ == "__main__":
    unittest.main()
