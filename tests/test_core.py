"""Tests standard tap features using the built-in SDK tests library.

Copyright (c) 2026 Edgar-Ramírez Mondragón
"""

from __future__ import annotations

from singer_sdk.testing import get_tap_test_class

from tap_forem.tap import TapForem

TestTapForem = get_tap_test_class(TapForem)
