import tempfile
import unittest
from pathlib import Path

from src.rts01_contract import run_contract


class SyntheticContractTest(unittest.TestCase):
    def test_runs_queue_to_remote_readback_as_one_correlation(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = run_contract(Path(directory))

        self.assertEqual(
            evidence["stages"],
            [
                "queue",
                "claim",
                "bounded_execution",
                "cas_writeback",
                "remote_readback",
            ],
        )
        self.assertTrue(all(evidence["status"].values()))
        self.assertEqual(evidence["claim"]["executor_id"], "synthetic-runner")
        self.assertTrue(evidence["bounded_execution"]["bounded"])
        self.assertEqual(evidence["bounded_execution"]["operation"], "fixture.transform")
        self.assertEqual(len(evidence["cas_writeback"]["result_sha256"]), 64)
        self.assertTrue(evidence["cas_writeback"]["idempotent"])
        self.assertTrue(evidence["remote_readback"]["matches_correlation"])


if __name__ == "__main__":
    unittest.main()
