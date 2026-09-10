# III-010 — Provenance-Aware Memory, Evidence & Retrieval Integrity Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** III-001 through III-009 and the ratified Phase II semantic architecture

## 1. Purpose

III-010 defines the integrity contract for evidence, source provenance, retrieval lineage, citation binding, evidence snapshots, source mutation, reproducibility, conflict, freshness, contamination, poisoning, knowledge lineage, and evidence-to-claim relationships.

The central requirement is:

```text
IF INFORMATION SUPPORTS A CONSEQUENTIAL CLAIM,
THE SYSTEM MUST BE ABLE TO ESTABLISH
WHICH INFORMATION WAS ACTUALLY USED,
WHICH VERSION IT HAD,
AND WHETHER THAT INFORMATION
REMAINS TRUSTWORTHY FOR THE CLAIM.
```

This contract answers:

```text
WHAT SOURCE PRODUCED THIS INFORMATION?
WHICH VERSION WAS USED?
WHEN WAS IT RETRIEVED?
WHAT EXACT EVIDENCE SUPPORTED THE CLAIM?
WAS THE EVIDENCE MODIFIED?
WAS IT CURRENT AT DECISION TIME?
CAN THE RETRIEVAL BE RECONSTRUCTED?
WAS THE SOURCE AUTHORITATIVE?
WERE CONFLICTING SOURCES PRESENT?
COULD THE EVIDENCE HAVE BEEN POISONED?
```

## 2. Evidence Identity

Every consequential evidence item should have a stable identifier.

```text
EVD-<ULID>
```

Evidence is distinct from its source:

```text
SOURCE ≠ EVIDENCE
```

Evidence should preserve its version, source reference, retrieval event, integrity state, scope, and provenance.

## 3. Source Identity and Version

A source may be a:

```text
document
database
API
web resource
tool
agent
human
sensor
knowledge object
evidence object
```

Where a source is versioned, the exact version used must be preserved. Where it is mutable and unversioned, an appropriate snapshot, immutable reference, or integrity representation should be retained.

Historical source state must remain distinguishable from current source state.

## 4. Source Authority

Source authority must be explicit.

Conceptual states include:

```text
AUTHORITATIVE
TRUSTED
SUPPORTED
UNVERIFIED
UNKNOWN
REVOKED
```

Retrieval ranking does not establish authority:

```text
HIGH RETRIEVAL RANK ≠ HIGH AUTHORITY
```

Authority must be resolved through the applicable authority/evidence contracts.

## 5. Evidence Snapshot

Consequential decisions should bind to the evidence actually observed at decision time.

```text
SOURCE
 ↓
RETRIEVAL
 ↓
EVIDENCE SNAPSHOT
 ↓
CLAIM
 ↓
DECISION
```

A later source mutation must not silently rewrite a historical decision.

## 6. Evidence-to-Claim Binding

Consequential claims must maintain machine-readable evidence relationships.

```yaml
claim:
  claim_id: CLM-...
  evidence_bindings:
    - evidence_ref: EVD-...
      relation: DIRECTLY_SUPPORTS
```

Conceptual support relations:

```text
DIRECTLY_SUPPORTS
PARTIALLY_SUPPORTS
CONTEXTUAL
CONTRADICTS
DOES_NOT_SUPPORT
UNKNOWN
```

The presence of a citation is not proof of support:

```text
HAS_CITATION ≠ HAS_SUFFICIENT_EVIDENCE
```

## 7. Evidence Sufficiency and Relevance

Evidence must be evaluated relative to the claim.

Relevant evidence may still be:

```text
stale
unauthorized
contradictory
low-quality
```

Therefore:

```text
RELEVANT ≠ TRUSTWORTHY
```

Sufficiency may depend on:

```text
directness
relevance
authority
freshness
independence
coverage
contradictions
claim complexity
```

## 8. Freshness and Expiration

Evidence freshness is contextual.

```yaml
freshness:
  observed_at: ...
  valid_from: ...
  valid_until: ...
  freshness_class: ...
```

Historical evidence may be valid for historical analysis while being unsuitable for current execution.

Expired evidence must not silently support a consequential current claim.

## 9. Integrity and Authenticity

Integrity asks:

```text
WAS THE OBSERVED CONTENT CHANGED?
```

Authenticity asks:

```text
DID THE CONTENT COME FROM THE CLAIMED SOURCE?
```

Therefore:

```text
INTEGRITY ≠ AUTHENTICITY
```

Appropriate mechanisms may include:

```text
content hash
immutable snapshot
signed artifact
version reference
trusted source identifier
```

## 10. Provenance Chain

Evidence lineage should be reconstructable:

```text
SOURCE
 ↓
RETRIEVAL
 ↓
EVIDENCE
 ↓
DERIVATION
 ↓
CLAIM
 ↓
DECISION
 ↓
EXECUTION
```

Every material transformation should preserve lineage.

## 11. Retrieval Identity

Every consequential retrieval should have an explicit identity.

```text
RET-<ULID>
```

A retrieval record should preserve:

```text
query
retriever
source set
retrieval method
ranking configuration where material
timestamp
context
result references
```

## 12. Retrieval Configuration

Material retrieval configuration must be versioned, including where applicable:

```text
embedding model
ranking model
search algorithm
filters
reranking
top-k
knowledge index version
```

Changed retrieval configuration can change evidence and therefore must remain reconstructable.

## 13. Retrieval Reproducibility

A consequential retrieval should be reproducible where technically feasible.

Reconstruction should identify:

```text
query
index/source version
retrieval configuration
retrieval timestamp
result set
```

The contract must distinguish deterministic reconstruction from historical snapshot recovery when external systems are mutable.

## 14. Retrieved vs Consumed Evidence

A system may retrieve many sources but use only some.

Therefore:

```text
RETRIEVED EVIDENCE ≠ CONSUMED EVIDENCE
```

Consequential provenance should identify evidence that actually influenced the claim or decision where this can be established.

## 15. Citation Integrity

A citation is integrity-valid only if the referenced evidence:

```text
exists
is identifiable
matches the cited source
has the expected version/snapshot
```

The system should detect:

```text
citation mismatch
citation incompleteness
unsupported claim
citation laundering
```

Citation laundering means a claim appears supported merely because it cites a source that does not actually support it.

## 16. Contradictory Evidence

Conflicting evidence must be represented explicitly.

```yaml
evidence_conflict:
  conflict_id: EVC-...
  claim_ref: CLM-...
  evidence_refs: []
  conflict_type: ...
  status: UNRESOLVED
  provenance_ref: ...
```

Resolution may consider:

```text
source authority
evidence quality
freshness
scope
independent corroboration
domain rules
explicit adjudication
```

Do not silently discard contradictory evidence.

## 17. Corroboration and Independence

Multiple sources do not automatically constitute independent evidence.

```text
MULTIPLE SOURCES ≠ INDEPENDENT SOURCES
```

Where material, preserve source-dependency relationships:

```text
SOURCE A
 ↓
ARTICLE B
 ↓
SUMMARY C
 ↓
CLAIM D
```

This prevents duplicated upstream information from being counted as independent corroboration.

## 18. Evidence Confidence

Confidence may be represented, but:

```text
HIGH CONFIDENCE
≠
HIGH AUTHORITY
≠
TRUTH
```

Evidence quality should remain multidimensional:

```text
authority
relevance
freshness
integrity
authenticity
independence
directness
completeness
```

## 19. Evidence Contamination

Evidence contamination includes:

```text
evaluation leakage
model-generated synthetic content
feedback loops
circular citations
data poisoning
source contamination
```

Contamination should be explicitly representable and testable.

## 20. Circular Evidence

The system should detect cycles such as:

```text
CLAIM A
 ↓
SOURCE B
 ↓
SOURCE C
 ↓
CLAIM A
```

Such a cycle is not independent corroboration.

## 21. Retrieval Poisoning

Retrieval must be tested against:

```text
keyword stuffing
authority impersonation
prompt injection
false citations
duplicate poisoning
ranking manipulation
malicious metadata
```

Potential detection signals include:

```text
source authority mismatch
content anomalies
duplicate provenance
unexpected instruction patterns
conflicting metadata
suspicious source relationships
```

Retrieval ranking is not a security boundary.

## 22. Evidence as Data, Not Control

Evidence may contain instructions.

Those instructions remain content unless explicitly authorized as control-plane input.

```text
EVIDENCE TEXT ≠ SYSTEM INSTRUCTION
```

Likewise:

```text
AGENT ASSERTION ≠ INDEPENDENT EVIDENCE
TOOL OUTPUT ≠ TRUTH
```

Tool-derived evidence must preserve tool identity, invocation, parameters, result, timestamp, and provenance.

## 23. Evidence Transformation

Evidence may be transformed through:

```text
OCR
parsing
summarization
translation
normalization
extraction
embedding
chunking
graph construction
```

Material transformations must preserve lineage.

Conceptually:

```text
SOURCE
 ↓
RAW SNAPSHOT
 ↓
PARSED EVIDENCE
 ↓
CHUNK
 ↓
EMBEDDING
 ↓
RETRIEVAL
 ↓
CLAIM
```

## 24. OCR and Extraction

When evidence originates from an image, PDF, scan, or other extracted representation, preserve:

```text
original source
extraction method
extractor version
extracted representation
confidence/uncertainty where applicable
```

The extracted representation must not silently replace the original source identity.

## 25. Summarization

A summary is derived information:

```text
SUMMARY ≠ SOURCE
```

A consequential claim based on a summary should preserve the underlying source lineage where possible.

## 26. Embedding and Vector Lineage

Vector representations must preserve:

```text
source evidence
source version
embedding model
embedding version
generation time
index version
```

A vector is not an opaque replacement for its source.

For vector retrieval, preserve the material retrieval lineage:

```text
source
source version
embedding version
index version
query representation
retrieval configuration
```

## 27. Knowledge Graph Lineage

Knowledge graph nodes and edges derived from evidence must preserve:

```text
source refs
evidence refs
derivation process
version
timestamp
```

A graph edge is not authoritative merely because it exists in the graph.

## 28. Evidence-to-Knowledge Binding

Derived knowledge must preserve the evidence from which it was produced:

```text
EVIDENCE
 ↓
DERIVATION
 ↓
KNOWLEDGE OBJECT
```

Knowledge objects must remain linked to contributing evidence versions.

## 29. Source Mutation and Revocation

The system must distinguish:

```text
WHAT THE SOURCE SAYS NOW
```

from:

```text
WHAT THE SYSTEM OBSERVED THEN
```

A source may later be:

```text
revoked
corrected
deprecated
compromised
```

Current trust state may change without erasing historical usage.

## 30. Evidence Re-evaluation

When a source is materially changed or revoked:

```text
SOURCE CHANGE
 ↓
AFFECTED EVIDENCE
 ↓
AFFECTED CLAIMS
 ↓
AFFECTED DECISIONS
 ↓
RE-EVALUATION
```

The impact-analysis mechanism remains implementation-specific.

## 31. Evidence Invalidation and Retraction

Evidence may be invalidated because of:

```text
source authenticity failure
integrity failure
provenance failure
material correction
policy revocation
contamination
expiration
```

Retractions should preserve:

```text
original evidence
retraction event
new source state
affected claims
affected decisions
```

Do not simply delete the old evidence.

## 32. Evidence Access and Least-Evidence Principle

Evidence access must respect:

```text
scope
authority
sensitivity
purpose
agent role
```

Where practical, agents should receive only evidence necessary for their task.

This reduces:

```text
context pollution
privacy exposure
attack surface
irrelevant evidence
```

## 33. Evidence Auditability

An authorized evaluator should be able to answer:

```text
Which evidence supported this claim?
Which source produced it?
Which version was used?
When was it retrieved?
Was it transformed?
Was it contradicted?
Was it later invalidated?
```

## 34. Historical Replay

The system should distinguish:

```text
HISTORICAL REPLAY
→ reproduce what was available then

CURRENT RETRIEVAL
→ retrieve what is available now
```

Current retrieval must never be silently presented as historical evidence.

## 35. Retrieval Cache Integrity

Cached results should preserve:

```text
query
retrieval configuration
source versions
created_at
expiry
integrity information
```

Cache entries must be invalidated when material context changes:

```text
source version
authority
policy
freshness
index version
retrieval configuration
```

## 36. Self-Critique Integration

Self-critique should inspect:

```text
evidence used
evidence omitted
source authority
citation bindings
freshness
conflicts
retrieval configuration
```

It should identify unsupported or weakly supported claims.

Critique remains evidence, not automatic approval.

## 37. Adversarial Verification Integration

The adversarial verifier should attack:

```text
false source
stale source
conflicting source
poisoned document
citation mismatch
source mutation
retrieval manipulation
knowledge graph corruption
vector index poisoning
```

Attack results become provenance records and, where appropriate, regression tests.

## 38. Evidence Benchmarks

Maintain at least:

```text
1. SOURCE INTEGRITY
2. RETRIEVAL INTEGRITY
3. CLAIM SUPPORT
4. PROVENANCE RECONSTRUCTION
5. ADVERSARIAL EVIDENCE RESILIENCE
```

Each remains separately measurable.

## 39. Evidence Reconstruction Benchmark

Given a historical claim, an independent evaluator should be able to reconstruct:

```text
claim
evidence used
source
source version
retrieval event
transformation chain
authority state
freshness state
conflicts
decision dependency
```

## 40. Evidence Failure Taxonomy

Potential failure classes:

```text
SOURCE_UNKNOWN
SOURCE_UNAUTHORIZED
SOURCE_CHANGED
SOURCE_REVOKED
EVIDENCE_MISSING
EVIDENCE_STALE
EVIDENCE_CONFLICT
EVIDENCE_UNSUPPORTED
PROVENANCE_BROKEN
RETRIEVAL_NON_REPRODUCIBLE
CITATION_MISMATCH
CITATION_INCOMPLETE
SOURCE_DEPENDENCY_HIDDEN
EVIDENCE_POISONED
EVIDENCE_CONTAMINATED
```

## 41. Evidence Incident

A consequential integrity failure should produce an incident record:

```yaml
evidence_incident:
  incident_id: EVI-...
  evidence_refs: []
  failure_type: ...
  affected_claims: []
  affected_decisions: []
  severity: ...
  remediation: ...
  provenance_ref: ...
```

## 42. Downstream Impact

When evidence becomes invalid:

```text
INVALID EVIDENCE
 ↓
CLAIMS USING EVIDENCE
 ↓
DECISIONS USING CLAIMS
 ↓
EXECUTIONS USING DECISIONS
```

The system should support identifying affected downstream objects.

## 43. Evidence Repair and Regression

Repair may involve:

```text
new source
new evidence snapshot
corrected extraction
updated provenance
re-evaluation
decision review
```

Repair must not erase the original integrity failure.

Known evidence failures should become regression tests.

## 44. Evidence Governance

Changes to:

```text
source authority
evidence policy
retrieval policy
trust classification
retention
```

must be governed through the applicable authority and lifecycle contracts.

## 45. Core Invariants

### Invariant 1
Every consequential evidence item has an explicit identity.

### Invariant 2
Evidence is distinct from its source.

### Invariant 3
Source authority is explicit.

### Invariant 4
Retrieval rank does not establish authority.

### Invariant 5
Evidence versions remain reconstructable where required.

### Invariant 6
Consequential claims bind to evidence explicitly.

### Invariant 7
Citation presence does not prove evidence sufficiency.

### Invariant 8
Retrieved evidence is distinct from consumed evidence.

### Invariant 9
Freshness is contextual.

### Invariant 10
Integrity is distinct from authenticity.

### Invariant 11
Evidence transformations preserve lineage.

### Invariant 12
Summaries do not replace source identity.

### Invariant 13
Embeddings do not replace source lineage.

### Invariant 14
Knowledge graph relationships preserve evidence lineage.

### Invariant 15
Conflicting evidence is explicitly represented.

### Invariant 16
Multiple sources do not automatically constitute independent corroboration.

### Invariant 17
Agent assertions are not automatically independent evidence.

### Invariant 18
Tool output is not automatically truth.

### Invariant 19
Evidence text does not automatically become control-plane instruction.

### Invariant 20
Historical evidence remains distinguishable from current source state.

### Invariant 21
Source revocation does not silently erase historical usage.

### Invariant 22
Evidence invalidation is explicit.

### Invariant 23
Historical replay is distinct from current retrieval.

### Invariant 24
Retrieval cache results cannot silently override current integrity requirements.

### Invariant 25
Citation laundering must be detectable.

### Invariant 26
Evidence quality is multi-dimensional.

### Invariant 27
Confidence does not substitute for evidence quality.

### Invariant 28
Implementation must not invent evidence semantics.

## 46. Required Tests

The reference implementation must test:

```text
evidence identity
evidence version
source identity
source version
source authority
retrieval identity
retrieval configuration
retrieval reproducibility
retrieved vs consumed evidence
citation binding
citation completeness
unsupported claim detection
contradictory evidence
corroboration
source dependency
evidence independence
evidence integrity
evidence authenticity
evidence transformation
OCR lineage
summarization lineage
embedding lineage
vector retrieval lineage
knowledge graph lineage
source mutation
source revocation
evidence invalidation
evidence retraction
evidence recovery
retrieval cache integrity
cache invalidation
citation laundering
retrieval poisoning
evidence contamination
historical replay
```

## 47. Falsification Cases

Deliberately attempt:

```text
modify source after retrieval
reuse stale evidence
forge source identity
forge source authority
change evidence without changing version
cite unrelated source
cite source that contradicts the claim
inflate evidence count using duplicate sources
hide source dependency
poison vector index
poison knowledge graph
inject instructions into evidence
make agent output appear independent
erase invalidated evidence
replay current evidence as historical evidence
use stale cache after source revocation
break evidence-to-claim binding
```

## 48. Deferred Decisions

III-010 intentionally does not freeze:

- exact provenance database;
- content-addressable storage;
- hashing/signature implementation;
- retrieval engine;
- vector database;
- graph database;
- citation extraction implementation;
- source-authority registry;
- freshness algorithm;
- evidence-quality scoring;
- conflict-resolution algorithm;
- source-dependency graph implementation;
- replay infrastructure;
- exact evidence schema syntax.

These remain engineering decisions unless they change semantic meaning.

## 49. Exit Criteria

- [x] Evidence identity defined
- [x] Evidence version defined
- [x] Evidence snapshot defined
- [x] Source identity and version defined
- [x] Source authority defined
- [x] Evidence-to-claim binding defined
- [x] Evidence sufficiency and relevance defined
- [x] Freshness and expiration defined
- [x] Integrity/authenticity distinction defined
- [x] Provenance chain defined
- [x] Retrieval identity and configuration defined
- [x] Retrieval reproducibility defined
- [x] Retrieved/consumed distinction defined
- [x] Citation integrity and completeness defined
- [x] Contradictory evidence defined
- [x] Corroboration and independence defined
- [x] Evidence contamination defined
- [x] Retrieval poisoning defined
- [x] Tool/agent-derived evidence boundaries defined
- [x] Transformation lineage defined
- [x] OCR, summary, embedding, vector and graph lineage defined
- [x] Source mutation/revocation defined
- [x] Evidence invalidation/retraction defined
- [x] Evidence access and least-evidence principle defined
- [x] Historical replay defined
- [x] Cache integrity defined
- [x] Self-critique integration defined
- [x] Adversarial verification integration defined
- [x] Evidence benchmarks defined
- [x] Reconstruction benchmark defined
- [x] Failure taxonomy defined
- [x] Incident and downstream impact handling defined
- [x] Repair and regression defined
- [x] Invariants defined
- [x] Required tests defined
- [x] Falsification cases defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation.

## 50. Next Contract

**III-011 — Multi-Agent Coordination, Delegation & Trust Boundary Contract**

III-011 will formalize:

```text
agent discovery
agent selection
coordination
task decomposition
delegation
authority propagation
authority containment
handoff
shared context
message integrity
agent trust
trust updates
cross-agent verification
conflict resolution
coordination failure
agent isolation
agent compromise
collusion resistance
```

The central requirement will be:

```text
COORDINATION MUST NOT
TURN DISTRIBUTED CAPABILITY
INTO UNCONTROLLED DISTRIBUTED AUTHORITY.
```
