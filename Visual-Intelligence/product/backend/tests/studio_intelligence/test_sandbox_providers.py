"""
Unit tests for Sandbox Providers & failure injection simulations.
"""

import pytest
from src.studio_intelligence.sandbox_providers import (
    SandboxSocialProvider,
    SandboxAnalyticsProvider,
    SandboxAssetProvider,
    SandboxNotificationProvider,
    SandboxSchedulingProvider,
)
from src.studio_intelligence.exceptions import ProviderRuntimeError


def test_sandbox_social_provider_success_and_failures():
    provider = SandboxSocialProvider()
    post = provider.publish_post(
        client_id="client_nocap",
        campaign_id="camp_1",
        content="Autumn Streetwear Collection",
        media_urls=["https://assets.nocap.internal/img1.jpg"],
    )
    assert post["status"] == "PUBLISHED"
    assert post["post_id"].startswith("post_")

    analytics = provider.get_post_analytics("client_nocap", post["post_id"])
    assert analytics["impressions"] == 15000.0

    # Failure Injection 1: Rate limit 429
    provider.should_fail_rate_limit = True
    with pytest.raises(ProviderRuntimeError, match="429"):
        provider.publish_post("client_nocap", "camp_1", "New content", [])
    provider.should_fail_rate_limit = False

    # Failure Injection 2: Duplicate post 409
    provider.should_fail_duplicate = True
    with pytest.raises(ProviderRuntimeError, match="409"):
        provider.publish_post(
            "client_nocap", "camp_1", "Autumn Streetwear Collection", []
        )


def test_sandbox_asset_notification_scheduling_providers():
    asset_prov = SandboxAssetProvider()
    res = asset_prov.store_asset("client_beta", "logo.png", b"12345", "image/png")
    assert res["size_bytes"] == 5

    notif_prov = SandboxNotificationProvider()
    nres = notif_prov.send_notification("client_beta", "admin@beta.internal", "Campaign Approved")
    assert nres["status"] == "SENT"

    sched_prov = SandboxSchedulingProvider()
    sres = sched_prov.schedule_publication("client_beta", "post_123", 1700000000.0)
    assert sres["status"] == "SCHEDULED"
    assert sched_prov.cancel_scheduled_publication("client_beta", sres["schedule_id"])
