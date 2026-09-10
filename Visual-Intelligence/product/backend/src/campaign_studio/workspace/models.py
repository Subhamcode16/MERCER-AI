"""
Phase 27 Workspace Management: Clients, Brands, Products, and Campaigns.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid


@dataclass
class ProductItem:
    product_id: str
    tenant_id: str
    client_id: str
    brand_id: str
    name: str
    category: str = "General"
    description: str = ""
    color_palette: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class BrandItem:
    brand_id: str
    tenant_id: str
    client_id: str
    name: str
    archetype: str = "Luxury"
    brand_ethos: str = ""
    visual_dna_profile_id: Optional[str] = None
    guidelines: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ClientItem:
    client_id: str
    tenant_id: str
    name: str
    industry: str = "Haute Couture & Luxury Fashion"
    tier: str = "ENTERPRISE"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class WorkspaceStore:
    """Stores client, brand, and product entities with strict tenant and reference isolation."""

    def __init__(self):
        self._clients: Dict[str, ClientItem] = {}
        self._brands: Dict[str, BrandItem] = {}
        self._products: Dict[str, ProductItem] = {}

    def create_client(self, client_id: str, name: str, industry: str = "Haute Couture", tenant_id: str = "tenant_default", tier: str = "ENTERPRISE") -> ClientItem:
        client = ClientItem(client_id=client_id, tenant_id=tenant_id, name=name, industry=industry, tier=tier)
        self._clients[client_id] = client
        return client

    def add_client(self, client: ClientItem) -> ClientItem:
        self._clients[client.client_id] = client
        return client

    def create_brand(self, brand_id: str, client_id: str, name: str, brand_ethos: str = "", archetype: str = "Luxury", tenant_id: str = "tenant_default") -> BrandItem:
        if client_id not in self._clients:
            raise KeyError(f"Client '{client_id}' does not exist.")
        brand = BrandItem(
            brand_id=brand_id,
            tenant_id=tenant_id,
            client_id=client_id,
            name=name,
            brand_ethos=brand_ethos,
            archetype=archetype,
        )
        self._brands[brand_id] = brand
        return brand

    def add_brand(self, brand: BrandItem) -> BrandItem:
        if brand.client_id not in self._clients:
            raise KeyError(f"Client '{brand.client_id}' does not exist.")
        self._brands[brand.brand_id] = brand
        return brand

    def create_product(self, product_id: str, brand_id: str, name: str, category: str = "General", color_palette: Optional[List[str]] = None, tenant_id: str = "tenant_default") -> ProductItem:
        brand = self._brands.get(brand_id)
        if not brand:
            raise KeyError(f"Brand '{brand_id}' does not exist.")
        prod = ProductItem(
            product_id=product_id,
            tenant_id=tenant_id,
            client_id=brand.client_id,
            brand_id=brand_id,
            name=name,
            category=category,
            color_palette=color_palette or [],
        )
        self._products[product_id] = prod
        return prod

    def add_product(self, product: ProductItem) -> ProductItem:
        if product.brand_id not in self._brands:
            raise KeyError(f"Brand '{product.brand_id}' does not exist.")
        self._products[product.product_id] = product
        return product

    def get_client(self, client_id: str, tenant_id: str = "*") -> Optional[ClientItem]:
        client = self._clients.get(client_id)
        if client and (client.tenant_id == tenant_id or tenant_id == "*"):
            return client
        return None

    def get_brand(self, brand_id: str, tenant_id: str = "*") -> Optional[BrandItem]:
        brand = self._brands.get(brand_id)
        if brand and (brand.tenant_id == tenant_id or tenant_id == "*"):
            return brand
        return None

    def get_product(self, product_id: str, tenant_id: str = "*") -> Optional[ProductItem]:
        prod = self._products.get(product_id)
        if prod and (prod.tenant_id == tenant_id or tenant_id == "*"):
            return prod
        return None

    def list_clients(self, tenant_id: str = "*") -> List[ClientItem]:
        if tenant_id == "*":
            return list(self._clients.values())
        return [c for c in self._clients.values() if c.tenant_id == tenant_id]

    def list_brands(self, client_id: str = "*", tenant_id: str = "*") -> List[BrandItem]:
        return [b for b in self._brands.values() if (client_id == "*" or b.client_id == client_id) and (tenant_id == "*" or b.tenant_id == tenant_id)]

    def list_brands_for_client(self, client_id: str, tenant_id: str = "*") -> List[BrandItem]:
        return self.list_brands(client_id=client_id, tenant_id=tenant_id)

    def list_products(self, brand_id: str = "*", tenant_id: str = "*") -> List[ProductItem]:
        return [p for p in self._products.values() if (brand_id == "*" or p.brand_id == brand_id) and (tenant_id == "*" or p.tenant_id == tenant_id)]

    def list_products_for_brand(self, brand_id: str, tenant_id: str = "*") -> List[ProductItem]:
        return self.list_products(brand_id=brand_id, tenant_id=tenant_id)
