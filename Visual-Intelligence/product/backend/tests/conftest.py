"""
Root pytest configuration for Visual Intelligence product backend tests.
Ensures src/ directory is on sys.path.
"""

import sys
from pathlib import Path

backend_src = Path(__file__).resolve().parent.parent / "src"
if str(backend_src) not in sys.path:
    sys.path.insert(0, str(backend_src))
