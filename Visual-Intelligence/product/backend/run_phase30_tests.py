"""
Test runner script for Phase 30 Institutional Intelligence test suite.
"""
import sys
import pathlib
import pytest

src_path = str(pathlib.Path(__file__).resolve().parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

if __name__ == "__main__":
    test_target = str(pathlib.Path(__file__).resolve().parent / "tests" / "institutional_intelligence")
    ret = pytest.main([test_target, "-v", "--tb=short"])
    sys.exit(ret)
