"""
Unit tests for Provider Contracts interfaces.
"""

from src.studio_intelligence.provider_contracts import (
    ISocialProvider,
    IAnalyticsProvider,
    IAssetProvider,
    INotificationProvider,
    ISchedulingProvider,
)


def test_provider_contracts_abstract():
    assert hasattr(ISocialProvider, "publish_post")
    assert hasattr(IAnalyticsProvider, "fetch_campaign_metrics")
    assert hasattr(IAssetProvider, "store_asset")
    assert hasattr(INotificationProvider, "send_notification")
    assert hasattr(ISchedulingProvider, "schedule_publication")
