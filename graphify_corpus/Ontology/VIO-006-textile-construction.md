---
Title: Textile & Construction Ontology
ID: VIO-006
Status: Draft
---

# VIO-006: Textile & Construction

This ontology maps the physical makeup of a garment—how it is constructed, woven, and embroidered. 

## 1. Domain Purpose
To strictly classify raw materials, weaves, embroidery techniques, and structural motifs.

## 2. Core Hierarchy

```text
Textile Construction
├── Fabric Base
│   ├── Silk
│   ├── Cotton
│   ├── Linen
│   ├── Organza
│   ├── Tissue
│   └── Chiffon
├── Weave Technique
│   ├── Banarasi
│   ├── Kanjeevaram
│   ├── Paithani
│   ├── Chanderi
│   └── Tussar
├── Embroidery & Embellishment
│   ├── Zardosi
│   ├── Gota Patti
│   ├── Mirror Work
│   ├── Aari
│   └── Threadwork
└── Structural Elements
    ├── Zari (Metallic Thread)
    ├── Borders (Heavy/Light)
    └── Pallu (End-piece)
```

## 3. Node Definitions

- **Banarasi:** A rich weaving technique originating in Varanasi, known for heavy brocade, gold/silver zari, and intricate floral/foliate motifs.
- **Zari:** Metallic thread (usually gold or silver) woven into the fabric to create patterns.

## 4. Usage in VIF
Station 3 (Textile & Texture Engine) outputs claims mapped directly to nodes within this taxonomy.

*Example Claim:*
`Subject: Garment, Predicate: Weave_Technique, Value: Banarasi`
