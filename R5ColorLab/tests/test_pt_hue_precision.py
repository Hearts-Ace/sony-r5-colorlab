"""Regression for the retained Edit half-index counterexample."""
import json
from pathlib import Path
import unittest
import numpy as np
import baseline
from edit_color_pipeline import RuntimeColor


class PTHuePrecisionTests(unittest.TestCase):
    def test_half_index_matches_retained_edit_capture(self):
        m=RuntimeColor.from_capture(*baseline.resolve(baseline.V45_ID))
        p=np.tile(np.array([4208,1574,6937],np.uint16),(1,9,1))
        np.testing.assert_array_equal(m.sectors(p),np.full((1,9),59))
        np.testing.assert_array_equal(m.color_only(p),np.tile([16383,9795,16383],(1,9,1)))

    def test_formal_platforms_have_identical_constraints(self):
        root=Path(__file__).resolve().parents[1]
        mac=json.loads((root/'web/formal_profile.json').read_text())
        amd=json.loads((root/'amd/formal_profile.json').read_text())
        self.assertEqual(mac['options'],amd['options'])
        self.assertEqual(mac['settings'],amd['settings'])
        self.assertEqual(amd['cpu_threads'],10)
        self.assertEqual(amd['batch_concurrency'],3)

if __name__=='__main__':unittest.main()
