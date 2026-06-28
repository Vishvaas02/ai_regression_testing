from __future__ import annotations

import unittest

from llm_test_framework.suite import SuiteLoadError, parse_suite


class SuiteTests(unittest.TestCase):
    def test_parse_suite_applies_defaults(self) -> None:
        suite = parse_suite(
            {
                "name": "demo",
                "defaults": {"repeats": 2, "assertions": [{"type": "safe_response"}]},
                "cases": [{"id": "one", "prompt": "hello"}],
            }
        )
        self.assertEqual(suite.name, "demo")
        self.assertEqual(suite.cases[0].repeats, 2)
        self.assertEqual(suite.cases[0].assertions[0]["type"], "safe_response")

    def test_parse_suite_requires_cases(self) -> None:
        with self.assertRaises(SuiteLoadError):
            parse_suite({"name": "bad", "cases": []})


if __name__ == "__main__":
    unittest.main()

