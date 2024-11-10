from dataclasses import dataclass

import pytest  # noqa: F401

from sheepy.parser.clipboard_parser import check_for_imdb_id


class TestParser:
    def test_match_id(self):
        @dataclass
        class TestCase:
            name: str
            input: str
            expected: bool

        testcases: list[TestCase] = [
            TestCase(
                name="7 digits valid id; should match", input="tt1234567", expected=True
            ),
            TestCase(
                name="8 digits valid id; should match",
                input="tt12345678",
                expected=True,
            ),
            TestCase(name="9 digits; should fail", input="tt123456789", expected=False),
            TestCase(name="6 digits; should fail", input="tt123456", expected=False),
            TestCase(
                name="only 7 numbers; should fail", input="1234567", expected=False
            ),
            TestCase(
                name="only 8 numbers; should fail", input="12345678", expected=False
            ),
            TestCase(
                name="mixed letters and digits; should fail",
                input="t123t4567",
                expected=False,
            ),
        ]
        for case in testcases:
            actual = check_for_imdb_id(case.input)
            assert actual == case.expected, f"error in testcase {case.name}"
