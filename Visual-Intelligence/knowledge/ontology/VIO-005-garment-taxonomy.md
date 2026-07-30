---
Title: Garment Taxonomy Ontology
ID: VIO-005
Status: Draft
---

# VIO-005: Garment Taxonomy

This ontology defines the strict hierarchy of fashion garments. It represents *what* the subject is, isolated from how it is constructed or styled.

## 1. Domain Purpose
To strictly classify garments into mutually exclusive and logically exhaustive hierarchies.

## 2. Core Hierarchy

```text
Garment
├── Tops
│   ├── Blouse
│   ├── Kurti
│   ├── Shirt
│   └── Tunic
├── Bottoms
│   ├── Trouser
│   ├── Skirt
│   ├── Salwar
│   └── Lehenga
├── Ensembles
│   ├── Saree
│   ├── Suit
│   ├── Gown
│   └── Co-ord Set
└── Accessories (Structural)
    └── Dupatta
```

## 3. Node Definitions

- **Saree:** A draped ensemble garment consisting of a single continuous unstitched length of fabric, typically worn with a blouse and petticoat.
- **Lehenga:** A three-piece ensemble comprising a skirt (lehenga), blouse (choli), and drape (dupatta).
- **Blouse:** A fitted upper-body garment.

## 4. Usage in VIF
Station 2 (Base Garment Analysis) outputs claims mapped directly to nodes within this taxonomy.

*Example Claim:*
`Subject: Image, Predicate: Base_Garment, Value: Saree`
