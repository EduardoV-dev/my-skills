import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "assets"))
from validate_coverage import validate


class CoverageValidatorTests(unittest.TestCase):
    def setUp(self):
        self.plan = {"reviewers": [{"id": "core", "check_ids": ["GEN-004"]}]}
        self.results = {
            "reviewers": [{"id": "core", "files_reviewed": ["src/auth.ts"]}],
            "checks": [{
                "reviewer_id": "core",
                "id": "GEN-004",
                "status": "PASS",
                "evidence": "src/auth.ts:10-20",
            }],
            "findings": [],
        }

    def test_accepts_complete_evidenced_result(self):
        self.assertEqual(validate(self.plan, self.results), [])

    def test_reports_missing_check_result(self):
        self.results["checks"] = []
        self.assertIn("missing check result: GEN-004", validate(self.plan, self.results))

    def test_pass_requires_evidence(self):
        self.results["checks"] = [{
            "reviewer_id": "core", "id": "GEN-004", "status": "PASS"
        }]
        errors = validate(self.plan, self.results)
        self.assertIn("check GEN-004: PASS requires evidence", errors)

    def test_fail_requires_a_known_finding(self):
        check = self.results["checks"][0]
        check.update(status="FAIL", finding_ids=["F-1"])
        errors = validate(self.plan, self.results)
        self.assertIn("check GEN-004: unknown finding ID F-1", errors)


if __name__ == "__main__":
    unittest.main()
