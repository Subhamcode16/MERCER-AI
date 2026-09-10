"""
Phase 18 Provider Contracts.

Strict abstract base classes defining contract interfaces for Social, Analytics,
Asset, Notification, and Scheduling provider integrations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class ISocialProvider(ABC):
    """Abstract contract for Social media platform providers."""

    @abstractmethod
    def publish_post(
        self, client_id: str, campaign_id: str, content: str, media_urls: List[str]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_post_analytics(self, client_id: str, post_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete_post(self, client_id: str, post_id: str) -> bool:
        pass


class IAnalyticsProvider(ABC):
    """Abstract contract for Analytics platform providers."""

    @abstractmethod
    def fetch_campaign_metrics(
        self, client_id: str, campaign_id: str
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def fetch_channel_performance(
        self, client_id: str, channel: str
    ) -> Dict[str, Any]:
        pass


class IAssetProvider(ABC):
    """Abstract contract for Asset storage providers."""

    @abstractmethod
    def store_asset(
        self, client_id: str, asset_name: str, asset_bytes: bytes, mime_type: str
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_asset(self, client_id: str, asset_id: str) -> Optional[Dict[str, Any]]:
        pass


class INotificationProvider(ABC):
    """Abstract contract for Notification providers."""

    @abstractmethod
    def send_notification(
        self, client_id: str, recipient: str, message: str, channel: str = "email"
    ) -> Dict[str, Any]:
        pass


class ISchedulingProvider(ABC):
    """Abstract contract for Scheduling providers."""

    @abstractmethod
    def schedule_publication(
        self, client_id: str, post_id: str, publish_at_timestamp: float
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def cancel_scheduled_publication(
        self, client_id: str, schedule_id: str
    ) -> bool:
        pass
