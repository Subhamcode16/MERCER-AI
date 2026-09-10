"""
Tests for FROST Prototype Configuration, Data Models, and Key Setup.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pytest
from research.frost_prototype.models import FROSTConfig, KeyShare
from research.frost_prototype.signing import generate_test_key_set
from research.frost_prototype.participants import compute_lagrange_coefficient


def test_valid_frost_config():
    """Verify creating valid threshold configurations."""
    c1 = FROSTConfig(total_participants_n=3, threshold_t=2)
    assert c1.total_participants_n == 3
    assert c1.threshold_t == 2

    c2 = FROSTConfig(total_participants_n=5, threshold_t=3)
    assert c2.total_participants_n == 5
    assert c2.threshold_t == 3

    c3 = FROSTConfig(total_participants_n=4, threshold_t=4)
    assert c3.threshold_t == 4


def test_invalid_frost_config():
    """Verify invalid threshold configuration parameters raise ValueError."""
    with pytest.raises(ValueError, match="total_participants_n must be at least 1"):
        FROSTConfig(total_participants_n=0, threshold_t=1)

    with pytest.raises(ValueError, match="threshold_t must be at least 1"):
        FROSTConfig(total_participants_n=3, threshold_t=0)

    with pytest.raises(ValueError, match="cannot exceed total_participants_n"):
        FROSTConfig(total_participants_n=3, threshold_t=4)


def test_shamir_key_generation():
    """Verify synthetic 3-of-5 threshold key generation produces consistent Shares and Group Public Key."""
    group_pubkey, shares = generate_test_key_set(total_n=5, threshold_t=3)

    assert len(shares) == 5
    assert all(s.group_public_key == group_pubkey for s in shares.values())
    assert all(s.marker == "TEST_ONLY_SYNTHETIC_SHARE" for s in shares.values())
    assert sorted(shares.keys()) == [1, 2, 3, 4, 5]


def test_lagrange_coefficient_calculation():
    """Verify Lagrange coefficient computation for active signing sets."""
    # 2-of-3 signing set {1, 2}
    l1 = compute_lagrange_coefficient(1, [1, 2])
    l2 = compute_lagrange_coefficient(2, [1, 2])

    assert l1 > 0
    assert l2 > 0
