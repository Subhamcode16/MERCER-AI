"""
Phase 18 Sandbox Providers.

Deterministic, fully simulated sandbox provider implementations for
Social, Analytics, Asset, Notification, and Scheduling operations.
Supports failure injection (rate limits, timeouts, duplicates, stale data).
"""

from typing import Dict, Any, List, Optional
import time
import uuid

from src.studio_intelligence.provider_contracts import (
    ISocialProvider,
    IAnalyticsProvider,
    IAssetProvider,
    INotificationProvider,
    ISchedulingProvider,
)
from src.studio_intelligence.exceptions import ProviderRuntimeError


class SandboxSocialProvider(ISocialProvider):
    """Sandbox implementation of Social Provider."""

    def __init__(self):
        self.published_posts: Dict[str, Dict[str, Any]] = {}
        self.should_fail_rate_limit: bool = False
        self.should_fail_timeout: bool = False
        self.should_fail_duplicate: bool = False

    def publish_post(
        self, client_id: str, campaign_id: str, content: str, media_urls: List[str]
    ) -> Dict[str, Any]:
        if self.should_fail_rate_limit:
            raise ProviderRuntimeError("Provider 429: Rate limit exceeded.")
        if self.should_fail_timeout:
            raise ProviderRuntimeError("Provider 504: Gateway timeout.")
        if self.should_fail_duplicate and content in [p["content"] for p in self.published_posts.values()]:
            raise ProviderRuntimeError("Provider 409: Duplicate post detected.")

        post_id = f"post_{uuid.uuid4().hex[:10]}"
        record = {
            "post_id": post_id,
            "client_id": client_id,
            "campaign_id": campaign_id,
            "content": content,
            "media_urls": media_urls,
            "status": "PUBLISHED",
            "published_at": time.time(),
            "impressions": 15000.0,
            "engagements": 900.0,
            "clicks": 350.0,
        }
        self.published_posts[post_id] = record
        return record

    def get_post_analytics(self, client_id: str, post_id: str) -> Dict[str, Any]:
        post = self.published_posts.get(post_id)
        if not post:
            raise ProviderRuntimeError(f"Post '{post_id}' not found.")
        return {
            "post_id": post_id,
            "impressions": post["impressions"],
            "engagements": post["engagements"],
            "clicks": post["clicks"],
            "shares": 120.0,
            "saves": 80.0,
        }

    def delete_post(self, client_id: str, post_id: str) -> bool:
        if post_id in self.published_posts:
            del self.published_posts[post_id]
            return True
        return False


class SandboxAnalyticsProvider(IAnalyticsProvider):
    """Sandbox implementation of Analytics Provider."""

    def fetch_campaign_metrics(
        self, client_id: str, campaign_id: str
    ) -> Dict[str, Any]:
        return {
            "client_id": client_id,
            "campaign_id": campaign_id,
            "impressions": 25000.0,
            "engagements": 1400.0,
            "clicks": 620.0,
            "conversions": 45.0,
            "publishing_errors": 0.0,
            "approval_latency_sec": 3600.0,
        }

    def fetch_channel_performance(
        self, client_id: str, channel: str
    ) -> Dict[str, Any]:
        return {
            "client_id": client_id,
            "channel": channel,
            "reach": 50000.0,
            "avg_engagement_rate": 0.045,
        }


class SandboxAssetProvider(IAssetProvider):
    """Sandbox implementation of Asset Provider."""

    def __init__(self):
        self.assets: Dict[str, Dict[str, Any]] = {}

    def store_asset(
        self, client_id: str, asset_name: str, asset_bytes: bytes, mime_type: str
    ) -> Dict[str, Any]:
        asset_id = f"asset_{uuid.uuid4().hex[:10]}"
        record = {
            "asset_id": asset_id,
            "client_id": client_id,
            "asset_name": asset_name,
            "size_bytes": len(asset_bytes),
            "mime_type": mime_type,
            "storage_url": f"https://sandbox-assets.ilyren.internal/{client_id}/{asset_id}",
        }
        self.assets[asset_id] = record
        return record

    def get_asset(self, client_id: str, asset_id: str) -> Optional[Dict[str, Any]]:
        return self.assets.get(asset_id)


class SandboxNotificationProvider(INotificationProvider):
    """Sandbox implementation of Notification Provider."""

    def __init__(self):
        self.notifications_sent: List[Dict[str, Any]] = []

    def send_notification(
        self, client_id: str, recipient: str, message: str, channel: str = "email"
    ) -> Dict[str, Any]:
        record = {
            "notification_id": f"notif_{uuid.uuid4().hex[:8]}",
            "client_id": client_id,
            "recipient": recipient,
            "message": message,
            "channel": channel,
            "status": "SENT",
            "timestamp": time.time(),
        }
        self.notifications_sent.append(record)
        return record


class SandboxSchedulingProvider(ISchedulingProvider):
    """Sandbox implementation of Scheduling Provider."""

    def __init__(self):
        self.schedules: Dict[str, Dict[str, Any]] = {}

    def schedule_publication(
        self, client_id: str, post_id: str, publish_at_timestamp: float
    ) -> Dict[str, Any]:
        sched_id = f"sched_{uuid.uuid4().hex[:8]}"
        record = {
            "schedule_id": sched_id,
            "client_id": client_id,
            "post_id": post_id,
            "publish_at_timestamp": publish_at_timestamp,
            "status": "SCHEDULED",
        }
        self.schedules[sched_id] = record
        return record

    def cancel_scheduled_publication(
        self, client_id: str, schedule_id: str
    ) -> bool:
        if schedule_id in self.schedules:
            self.schedules[schedule_id]["status"] = "CANCELLED"
            return True
        return False
