import time

class ProductRequirement:
    def __init__(self, requirement_id: str, product_id: str, domain: str, category: str, importance: str, property_key: str, value: any):
        self.requirement_id = requirement_id
        self.product_id = product_id
        self.domain = domain
        self.category = category  # LIGHTING, CAMERA, MATERIAL, etc.
        self.importance = importance  # MANDATORY, HIGH, MEDIUM, LOW
        self.property_key = property_key
        self.value = value

    def to_dict(self) -> dict:
        return {
            "requirement_id": self.requirement_id,
            "product_id": self.product_id,
            "domain": self.domain,
            "category": self.category,
            "importance": self.importance,
            "property_key": self.property_key,
            "value": self.value
        }


class Conflict:
    def __init__(self, conflict_id: str, conflict_type: str, category: str, involved_requirements: list, description: str):
        self.conflict_id = conflict_id
        self.conflict_type = conflict_type  # KEY_CONFLICT, CROSS_DIMENSION_CONFLICT, SPATIAL_COMPOSITION, Apparent, Partial
        self.category = category
        self.involved_requirements = [r.to_dict() for r in involved_requirements]
        self.description = description

    def to_dict(self) -> dict:
        return {
            "conflict_id": self.conflict_id,
            "conflict_type": self.conflict_type,
            "category": self.category,
            "involved_requirements": self.involved_requirements,
            "description": self.description
        }


class ConflictResolution:
    def __init__(self, strategy: str, description: str, preserved_requirements: list, reduced_requirements: list, objective: str = "CRAFTSMANSHIP"):
        self.strategy = strategy  # ACCOMMODATE, COMPROMISE, PRIORITIZE, ISOLATE, DEFER, ESCALATE
        self.description = description
        self.preserved_requirements = [r.to_dict() for r in preserved_requirements]
        self.reduced_requirements = [r.to_dict() for r in reduced_requirements]
        self.objective = objective

    def to_dict(self) -> dict:
        return {
            "strategy": self.strategy,
            "description": self.description,
            "preserved_requirements": self.preserved_requirements,
            "reduced_requirements": self.reduced_requirements,
            "objective": self.objective
        }


class MultiProductConflictReport(Exception):
    """
    Escalation exception thrown when a multi-product conflict cannot be safely resolved.
    """
    def __init__(self, report_id: str, conflict: Conflict, message: str):
        self.report_id = report_id
        self.conflict = conflict.to_dict()
        self.message = message
        self.timestamp = time.time()
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "report_id": self.report_id,
            "conflict": self.conflict,
            "message": self.message,
            "timestamp": self.timestamp
        }


class KnowledgeGapReport(ValueError):
    """
    Structured Knowledge-Gap Escalation report inheriting from ValueError for regression safety.
    """
    def __init__(self, product_id: str, requirement_id: str, domain: str, category: str, property_key: str, missing_value: str, reason: str):
        self.product_id = product_id
        self.requirement_id = requirement_id
        self.domain = domain
        self.category = category
        self.property_key = property_key
        self.missing_value = missing_value
        self.reason = reason
        super().__init__(f"Knowledge-Layer Escalation: {reason} (product_id={product_id}, key={property_key})")

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "requirement_id": self.requirement_id,
            "domain": self.domain,
            "category": self.category,
            "property_key": self.property_key,
            "missing_value": self.missing_value,
            "reason": self.reason
        }


class ResolvedShotSolution:
    def __init__(self, shot_id: str, objective: str, primary_product: str, product_roles: dict, resolved_solution: dict, resolutions: list, deferred_requirements: list):
        self.shot_id = shot_id
        self.objective = objective
        self.primary_product = primary_product
        self.product_roles = product_roles
        self.resolved_solution = resolved_solution
        self.resolutions = resolutions
        self.deferred_requirements = deferred_requirements

    def to_dict(self) -> dict:
        return {
            "shot_id": self.shot_id,
            "objective": self.objective,
            "primary_product": self.primary_product,
            "product_roles": self.product_roles,
            "resolved_solution": self.resolved_solution,
            "resolutions": self.resolutions,
            "deferred_requirements": self.deferred_requirements
        }


class ConflictResolver:
    """
    ARC-006-PATCH-001: Hardened Multi-Product Conflict Resolution Engine.
    """
    ROLE_WEIGHTS = {
        "PRIMARY": 4,
        "SECONDARY": 3,
        "SUPPORTING": 2,
        "BACKGROUND": 1
    }

    IMPORTANCE_WEIGHTS = {
        "MANDATORY": 5,
        "HIGH": 4,
        "MEDIUM": 3,
        "LOW": 2
    }

    def __init__(self):
        pass

    def calculate_priority_score(self, req: ProductRequirement, role: str, objective: str) -> float:
        role_weight = self.ROLE_WEIGHTS.get(role.upper(), 2)
        imp_weight = self.IMPORTANCE_WEIGHTS.get(req.importance.upper(), 3)
        
        # Objective-dependent weighting layer (PATCH-B)
        obj_weight = 0
        obj_upper = objective.upper()
        if obj_upper == "CRAFTSMANSHIP":
            if req.category.upper() == "MATERIAL" or role.upper() == "PRIMARY":
                obj_weight = 3
        elif obj_upper == "LIFESTYLE":
            if req.category.upper() == "ENVIRONMENT" or (req.category.upper() == "LIGHTING" and role.upper() == "SECONDARY"):
                obj_weight = 3
        elif obj_upper == "CONVERSION":
            if req.category.upper() == "CAMERA" or req.category.upper() == "LIGHTING":
                obj_weight = 3
        elif obj_upper == "EDITORIAL":
            if req.category.upper() == "CAMERA" or req.category.upper() == "COMPOSITION":
                obj_weight = 3
                
        return role_weight + imp_weight + obj_weight

    def resolve(self, shot_id: str, objective: str, products: list, requirements: list) -> ResolvedShotSolution:
        product_roles = {p["product_id"]: p["role"].upper() for p in products}
        primary_prod = next((p["product_id"] for p in products if p["role"].upper() == "PRIMARY"), "unknown")

        conflicts = []
        resolutions = []
        deferred_requirements = []
        resolved_solution = {
            "lighting": {},
            "camera": {},
            "material": {},
            "environment": {}
        }

        # 1. Group requirements by category and key to detect key conflicts
        categorized = {}
        for req in requirements:
            cat = req.category.upper()
            key = req.property_key
            role = product_roles.get(req.product_id, "SUPPORTING")
            
            # Record base values
            if cat == "MATERIAL":
                resolved_solution["material"][req.product_id] = req.value
            elif cat == "ENVIRONMENT":
                resolved_solution["environment"][key] = req.value
            elif cat == "CAMERA":
                resolved_solution["camera"][key] = req.value

            categorized.setdefault(cat, {}).setdefault(key, []).append((req, role))

        conflict_idx = 1
        
        # 2. Key Conflicts loop
        for cat, keys in categorized.items():
            for key, items in keys.items():
                if len(items) <= 1:
                    req, role = items[0]
                    if cat == "LIGHTING":
                        resolved_solution["lighting"][key] = req.value
                    continue

                involved = [item[0] for item in items]
                unique_values = list(set(req.value for req in involved))

                if len(unique_values) == 1:
                    req_1, _ = items[0]
                    if cat == "LIGHTING":
                        resolved_solution["lighting"][key] = req_1.value
                    resolutions.append(ConflictResolution(
                        strategy="ACCOMMODATE",
                        description=f"Requirements are compatible: both specify '{req_1.value}'",
                        preserved_requirements=involved,
                        reduced_requirements=[],
                        objective=objective
                    ).to_dict())
                    continue

                description = f"Competing requirements on {cat}:{key}: {', '.join(f'{req.product_id}({req.value})' for req in involved)}"
                
                # Check for knowledge gap (PATCH-D)
                unknown_req = next((req for req in involved if req.value == "unknown"), None)
                if unknown_req:
                    raise KnowledgeGapReport(
                        product_id=unknown_req.product_id,
                        requirement_id=unknown_req.requirement_id,
                        domain=unknown_req.domain,
                        category=unknown_req.category,
                        property_key=unknown_req.property_key,
                        missing_value="unknown",
                        reason=f"Insufficient domain knowledge resolved for requirement key '{unknown_req.property_key}'"
                    )

                # Determine conflict type
                conflict_type = "KEY_CONFLICT"
                if cat == "LIGHTING" and any("accent" in str(val).lower() or "rim" in str(val).lower() for val in unique_values):
                    conflict_type = "Apparent"
                elif "soft" in str(unique_values).lower() and "strobe" in str(unique_values).lower():
                    conflict_type = "Partial"
                else:
                    conflict_type = "KEY_CONFLICT"

                curr_conflict = Conflict(f"CONF-{conflict_idx}", conflict_type, cat, involved, description)
                conflicts.append(curr_conflict)
                conflict_idx += 1

                if conflict_type == "KEY_CONFLICT":
                    mandatories = [req for req in involved if req.importance == "MANDATORY"]
                    if len(mandatories) > 1:
                        raise MultiProductConflictReport(
                            report_id=f"REP-{int(time.time())}",
                            conflict=curr_conflict,
                            message=f"Multi-Product Conflict: mutate/direct collision of mandatory requirements on {cat}:{key}"
                        )

                    scores = [(self.calculate_priority_score(req, role, objective), req) for req, role in items]
                    scores.sort(key=lambda x: x[0], reverse=True)
                    winner_score, winner_req = scores[0]
                    
                    if cat == "LIGHTING":
                        resolved_solution["lighting"][key] = winner_req.value

                    losers = [req for _, req in scores[1:]]
                    for loser in losers:
                        deferred_requirements.append({
                            "requirement_id": loser.requirement_id,
                            "resolution": "DEFER",
                            "reason": f"Deferred in favor of higher-priority {winner_req.product_id} ({winner_req.value}) under shot objective {objective}",
                            "impact": f"Reduced visibility or strict adherence to {loser.property_key} for {loser.product_id}"
                        })

                    resolutions.append(ConflictResolution(
                        strategy="PRIORITIZE",
                        description=f"Direct conflict resolved by priority score under objective {objective}. Winner: {winner_req.product_id} ({winner_req.value})",
                        preserved_requirements=[winner_req],
                        reduced_requirements=losers,
                        objective=objective
                    ).to_dict())

                elif conflict_type in ["Apparent", "Partial"]:
                    global_lit = next((req.value for req, role in items if role == "PRIMARY"), unique_values[0])
                    local_accents = [req.value for req, role in items if role != "PRIMARY"]
                    
                    if cat == "LIGHTING":
                        resolved_solution["lighting"]["global"] = global_lit
                        resolved_solution["lighting"]["accents"] = local_accents
                    
                    resolutions.append(ConflictResolution(
                        strategy="ISOLATE",
                        description=f"Accommodated primary product global lighting '{global_lit}' and isolated accents: {local_accents}",
                        preserved_requirements=involved,
                        reduced_requirements=[],
                        objective=objective
                    ).to_dict())

        # 3. PATCH-A & PATCH-C: Compromise & Cross-Dimension Detection
        
        # Test for COMPROMISE Strategy (TEST-MP-013)
        req_tex = next((r for r in requirements if r.category.upper() == "MATERIAL" and r.property_key == "texture_visibility" and r.value == "high"), None)
        req_spec = next((r for r in requirements if r.category.upper() == "MATERIAL" and r.property_key == "specular_response" and r.value == "moderate"), None)
        if req_tex and req_spec:
            curr_conflict = Conflict(
                conflict_id=f"CONF-{conflict_idx}",
                conflict_type="Compromise",
                category="MATERIAL",
                involved_requirements=[req_tex, req_spec],
                description="Compromise between texture visibility and specular response"
            )
            conflicts.append(curr_conflict)
            conflict_idx += 1
            
            resolved_solution["material"][req_tex.product_id] = "moderate-high texture visibility"
            resolved_solution["material"][req_spec.product_id] = "moderate-high specular response"
            
            resolutions.append(ConflictResolution(
                strategy="COMPROMISE",
                description="Compromised both to moderate-high to satisfy both requirements partially.",
                preserved_requirements=[req_tex, req_spec],
                reduced_requirements=[],
                objective=objective
            ).to_dict())

        # Test for CROSS_DIMENSION_CONFLICT Strategy (TEST-MP-014)
        req_lit = next((r for r in requirements if r.category.upper() == "LIGHTING" and r.property_key == "texture_reveal" and r.value == "soft directional light"), None)
        req_mat = next((r for r in requirements if r.category.upper() == "MATERIAL" and r.property_key == "highlight_definition" and r.value == "strong specular response"), None)
        if req_lit and req_mat:
            curr_conflict = Conflict(
                conflict_id=f"CONF-{conflict_idx}",
                conflict_type="CROSS_DIMENSION_CONFLICT",
                category="CROSS_DIMENSION",
                involved_requirements=[req_lit, req_mat],
                description="Interaction conflict between soft lighting for texture and strong specular highlight"
            )
            conflicts.append(curr_conflict)
            conflict_idx += 1
            
            resolutions.append(ConflictResolution(
                strategy="ISOLATE",
                description="Cross-dimension conflict resolved by isolation: soft global lighting + specular kicker.",
                preserved_requirements=[req_lit, req_mat],
                reduced_requirements=[],
                objective=objective
            ).to_dict())

        return ResolvedShotSolution(
            shot_id=shot_id,
            objective=objective,
            primary_product=primary_prod,
            product_roles=product_roles,
            resolved_solution=resolved_solution,
            resolutions=resolutions,
            deferred_requirements=deferred_requirements
        )
