"""
Pytest configuration for security_substrate test package.
Ensures backend src/ directory is inserted into sys.path.
"""

import sys
from pathlib import Path

# Path(__file__) = tests/security_substrate/conftest.py
# .parent = tests/security_substrate
# .parent.parent = tests
# .parent.parent.parent = backend
src_dir = Path(__file__).resolve().parent.parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
