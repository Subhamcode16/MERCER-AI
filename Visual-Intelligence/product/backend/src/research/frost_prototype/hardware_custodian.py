"""
Mock Hardware Custodian Abstraction for FROST Research Prototype.
Simulates hardware token key custody, device availability, PIN locking, share corruption, and timeouts.
STRICTLY MOCK / RESEARCH ABSTRACTION.
DOES NOT ACCESS YUBIKEY, PIV, TPM, HSM, SMART CARDS, OR REAL HARDWARE TOKENS.
"""

import threading
import time
from typing import Optional, Dict
from .models import KeyShare


class HardwareCustodianException(Exception):
    """Base exception for mock hardware custodian operations."""
    pass


class HardwareLockedException(HardwareCustodianException):
    """Raised when the simulated hardware token is locked or PIN is invalid."""
    pass


class HardwareUnavailableException(HardwareCustodianException):
    """Raised when the simulated hardware token is disconnected or unavailable."""
    pass


class CorruptedShareException(HardwareCustodianException):
    """Raised when the share stored in mock hardware is corrupted."""
    pass


class HardwareTimeoutException(HardwareCustodianException):
    """Raised when simulated hardware communication times out."""
    pass


class MockHardwareCustodian:
    """
    Mock Hardware Custodian interface.
    Provides isolated in-memory simulation of hardware-backed share storage & signing authorization.
    """
    def __init__(self, participant_id: int, key_share: KeyShare, pin: str = "123456"):
        self.participant_id = participant_id
        self._key_share = key_share
        self._pin = pin
        self._failed_pin_attempts = 0
        self._max_pin_attempts = 3
        self.is_locked = False
        self.is_connected = True
        self.is_corrupted = False
        self.simulated_delay_seconds = 0.0
        self.timeout_limit_seconds = 5.0
        self._lock = threading.RLock()

    def authenticate_and_fetch_share(self, provided_pin: str) -> KeyShare:
        """
        Simulates hardware PIN authentication and share retrieval.
        Raises HardwareUnavailableException, HardwareLockedException, HardwareTimeoutException, or CorruptedShareException.
        """
        with self._lock:
            if not self.is_connected:
                raise HardwareUnavailableException(f"Mock hardware device for participant {self.participant_id} is disconnected")

            if self.is_locked:
                raise HardwareLockedException(f"Mock hardware device for participant {self.participant_id} is locked due to PIN failures")

            if self.simulated_delay_seconds > self.timeout_limit_seconds:
                raise HardwareTimeoutException(f"Mock hardware response timeout ({self.simulated_delay_seconds}s > {self.timeout_limit_seconds}s limit)")

            if provided_pin != self._pin:
                self._failed_pin_attempts += 1
                if self._failed_pin_attempts >= self._max_pin_attempts:
                    self.is_locked = True
                    raise HardwareLockedException(f"Invalid PIN. Maximum attempts exceeded. Device {self.participant_id} is now LOCKED.")
                raise HardwareLockedException(f"Invalid PIN provided for mock hardware device {self.participant_id}")

            # Reset failed PIN count on successful authentication
            self._failed_pin_attempts = 0

            if self.is_corrupted:
                raise CorruptedShareException(f"Share data on mock hardware device {self.participant_id} is corrupted")

            if self.simulated_delay_seconds > 0:
                time.sleep(self.simulated_delay_seconds)

            return self._key_share

    def set_device_status(
        self,
        connected: Optional[bool] = None,
        locked: Optional[bool] = None,
        corrupted: Optional[bool] = None,
        delay_seconds: Optional[float] = None
    ) -> None:
        """
        Utility for testing hardware fault injection (disconnections, locks, share corruption, delays).
        """
        with self._lock:
            if connected is not None:
                self.is_connected = connected
            if locked is not None:
                self.is_locked = locked
            if corrupted is not None:
                self.is_corrupted = corrupted
            if delay_seconds is not None:
                self.simulated_delay_seconds = delay_seconds
