"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_standard_tap_tests

from tap_forem.tap import TapForem

SAMPLE_CONFIG = {
    "tag": "meltano",
}


def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapForem, config=SAMPLE_CONFIG)
    for test in tests:
        test()
