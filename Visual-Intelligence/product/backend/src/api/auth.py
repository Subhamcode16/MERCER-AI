"""
Phase 25 API Authentication and Identity Resolver.
"""
from typing import Optional, Dict, Any, List
from fastapi import Header, HTTPException, Security
from src.control_plane.models import OperatorIdentity, OperatorRole
from src.control_plane.context import OperatorContext

# Mock registry for operator authentication verification
OPERATOR_TOKEN_STORE: Dict[str, OperatorIdentity] = {
    "tok-curator-alpha": OperatorIdentity(
        operator_id="op-curator-01",
        username="lead_curator_elena",
        roles=[OperatorRole.LEAD_CURATOR],
        tenant_scope="tenant_atelier",
        allowed_clients=["client_alpha", "client_atelier_01"]
    ),
    "tok-sre-beta": OperatorIdentity(
        operator_id="op-sre-01",
        username="sre_alex",
        roles=[OperatorRole.SRE_ENGINEER],
        tenant_scope="*",
        allowed_clients=["*"]
    ),
    "tok-admin-root": OperatorIdentity(
        operator_id="op-admin-01",
        username="studio_admin_marcus",
        roles=[OperatorRole.STUDIO_ADMIN],
        tenant_scope="*",
        allowed_clients=["*"]
    ),
    "tok-director-gamma": OperatorIdentity(
        operator_id="op-director-01",
        username="creative_director_chloe",
        roles=[OperatorRole.CREATIVE_DIRECTOR],
        tenant_scope="tenant_streetwear",
        allowed_clients=["client_streetwear_01"]
    )
}

def authenticate_operator(
    authorization: Optional[str] = Header(None),
    x_tenant_id: Optional[str] = Header(None),
    x_client_id: Optional[str] = Header(None)
) -> OperatorContext:
    """Extracts and validates bearer token and constructs secure OperatorContext."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header.")

    token = authorization.replace("Bearer ", "").strip()
    if token not in OPERATOR_TOKEN_STORE:
        raise HTTPException(status_code=401, detail="Invalid or expired operator token.")

    identity = OPERATOR_TOKEN_STORE[token]
    tenant = x_tenant_id or identity.tenant_scope
    client = x_client_id or (identity.allowed_clients[0] if identity.allowed_clients else "*")

    return OperatorContext(
        operator_id=identity.operator_id,
        tenant_id=tenant,
        client_id=client,
        roles=identity.roles
    )
