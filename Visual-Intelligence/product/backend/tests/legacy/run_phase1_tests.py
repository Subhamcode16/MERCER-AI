"""
Test runner script for Phase 1 Security Substrate test suite.
"""

import sys
import pathlib
import pytest

src_path = str(pathlib.Path(__file__).resolve().parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

if __name__ == "__main__":
    ret = pytest.main(["tests/security_substrate", "-v"])
    sys.exit(ret)
