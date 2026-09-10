import re
import time
from prompt_compiler import PromptLinter

class SegmentNormalizer:
    """
    Deterministic normalizer stage to clean up punctuation, list joinings,
    and structural flaws introduced during targeted prompt editing.
    Runs between targeted editor and prompt linter.
    """
    @staticmethod
    def normalize_segment(text: str) -> str:
        # 1. Save trailing period state
        ends_with_dot = text.strip().endswith('.')

        # 2. Duplicate punctuation cleanup
        text = re.sub(r'\s*\.,\s*', ', ', text)
        text = re.sub(r',\s*,', ', ', text)
        text = re.sub(r'\.\s*\.', '. ', text)
        text = re.sub(r',\s*\.', ', ', text)

        # 3. Incorrect sentence joining (e.g. "silk. with visible" -> "silk with visible")
        text = re.sub(r'\.\s*with\b', ' with', text, flags=re.IGNORECASE)
        text = re.sub(r',\s*with\b', ' with', text, flags=re.IGNORECASE)

        # 4. Obvious duplicate semantic clauses separated by commas
        parts = [p.strip() for p in text.split(',')]
        seen = []
        for p in parts:
            if p and p.lower() not in [s.lower() for s in seen]:
                seen.append(p)
        text = ", ".join(seen)

        # 5. Clean up dangling formatting and restore period if appropriate
        text = re.sub(r'^[,\s.]+', '', text)
        text = re.sub(r'[,\s.]+$', '', text)
        
        # Remove duplicate spaces
        text = re.sub(r'\s+', ' ', text).strip()

        if ends_with_dot and text:
            text += '.'

        return text


class PromptDiff:
    def __init__(self, modified_segments: list, changes: list, unchanged_segments: list):
        self.modified_segments = modified_segments
        self.changes = changes
        self.unchanged_segments = unchanged_segments

    def to_dict(self) -> dict:
        return {
            "modified_segments": self.modified_segments,
            "changes": self.changes,
            "unchanged_segments": self.unchanged_segments
        }


class CorrectionPlan:
    def __init__(self, correction_id: str, evaluation_id: str, shot_id: str, failure: dict, cause: dict, affected_segments: list, preserve_segments: list, corrections: list, success_criteria: list, confidence: float):
        self.correction_id = correction_id
        self.evaluation_id = evaluation_id
        self.shot_id = shot_id
        self.failure = failure
        self.cause = cause
        self.affected_segments = affected_segments
        self.preserve_segments = preserve_segments
        self.corrections = corrections
        self.success_criteria = success_criteria
        self.confidence = confidence

    def to_dict(self) -> dict:
        return {
            "correction_id": self.correction_id,
            "evaluation_id": self.evaluation_id,
            "shot_id": self.shot_id,
            "failure": self.failure,
            "cause": self.cause,
            "affected_segments": self.affected_segments,
            "preserve_segments": self.preserve_segments,
            "corrections": self.corrections,
            "success_criteria": self.success_criteria,
            "confidence": self.confidence
        }


class IntelligenceGapReport:
    def __init__(self, report_id: str, failure_pattern: str, target_dimension: str, attempts_count: int, gap_hypothesis: str):
        self.report_id = report_id
        self.failure_pattern = failure_pattern
        self.target_dimension = target_dimension
        self.attempts_count = attempts_count
        self.gap_hypothesis = gap_hypothesis
        self.timestamp = time.time()

    def to_dict(self) -> dict:
        return {
            "report_id": self.report_id,
            "failure_pattern": self.failure_pattern,
            "target_dimension": self.target_dimension,
            "attempts_count": self.attempts_count,
            "gap_hypothesis": self.gap_hypothesis,
            "timestamp": self.timestamp
        }


class TargetedPromptEditor:
    """
    ARC-003: Targeted Prompt Editor.
    Receives an existing prompt and a CorrectionPlan, and edits ONLY permitted segments.
    Applies SegmentNormalizer and PromptLinter before final yield.
    """
    def parse_segments(self, prompt_str: str) -> dict:
        segments = {}
        pattern = r"^(SUBJECT|MATERIAL|LIGHTING|CAMERA|ENVIRONMENT|QUALITY|FORBIDDEN):\s*(.*?)$"
        for line in prompt_str.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                segments[match.group(1)] = match.group(2)
        return segments

    def rebuild_prompt(self, segments: dict) -> str:
        order = ["SUBJECT", "MATERIAL", "LIGHTING", "CAMERA", "ENVIRONMENT", "QUALITY", "FORBIDDEN"]
        return "\n".join(f"{seg}: {segments[seg]}" for seg in order if seg in segments)

    def calculate_locality(self, changes: list, original_prompt: str) -> float:
        """
        Lexical Correction Locality: measures the proportion of prompt words/tokens altered
        by a targeted correction.
        NOTE: This is an operational lexical approximation. It does not measure semantic scope.
        Future Enhancement: semantic_correction_locality will evaluate whether the semantic scope
        remained localized even when changed words count is large.
        """
        changed_words_count = 0
        for change in changes:
            changed_words_count += len(str(change.get("after", "")).split())
        total_words_count = len(original_prompt.split())
        return min(1.0, changed_words_count / max(1.0, total_words_count))

    def edit(self, existing_prompt: str, plan: CorrectionPlan) -> dict:
        segments = self.parse_segments(existing_prompt)
        original_segments = dict(segments)
        changes = []
        modified_segments = []

        # Validate that no protected segments are targeted for modification
        for corr in plan.corrections:
            seg = corr["segment"]
            if seg in plan.preserve_segments:
                raise ValueError(f"Constraint Violation: Operation attempts to modify protected segment '{seg}'")
            if seg not in plan.affected_segments:
                raise ValueError(f"Constraint Violation: Segment '{seg}' is not listed in plan's affected_segments")

        # Execute operations deterministically
        for corr in plan.corrections:
            seg = corr["segment"]
            op = corr["operation"].upper()
            target = corr.get("target", "")
            instruction = corr.get("instruction", "")

            before_val = segments.get(seg, "")
            after_val = before_val

            if op == "ADD":
                if before_val:
                    after_val = before_val + ", " + instruction
                else:
                    after_val = instruction
            elif op == "AUGMENT":
                if target and target in before_val:
                    after_val = before_val.replace(target, f"{target} with {instruction}")
                else:
                    after_val = before_val + ", " + instruction
            elif op == "REMOVE":
                if target in before_val:
                    after_val = before_val.replace(target, "").replace(", ,", ",").strip(", ")
            elif op == "REPLACE":
                if target in before_val:
                    after_val = before_val.replace(target, instruction)
                else:
                    after_val = instruction
            elif op in ["STRENGTHEN", "WEAKEN", "DE-EMPHASIZE"]:
                after_val = before_val + f" ({instruction})"

            segments[seg] = after_val
            modified_segments.append(seg)
            changes.append({
                "segment": seg,
                "operation": op,
                "before": before_val,
                "after": after_val
            })

        # Run Segment Normalizer on modified segments only
        normalized_segments = {}
        for s_name, s_val in segments.items():
            if s_name in modified_segments:
                normalized_segments[s_name] = SegmentNormalizer.normalize_segment(s_val)
            else:
                normalized_segments[s_name] = s_val

        modified_prompt = self.rebuild_prompt(normalized_segments)

        # Run linter on the modified prompt
        linter_warnings = PromptLinter.lint(modified_prompt)
        if any("prohibited" in w.lower() for w in linter_warnings):
            return {
                "success": False,
                "error": "Linter violation: Correction injected prohibited keywords.",
                "warnings": linter_warnings
            }

        # Calculate locality metric
        locality = self.calculate_locality(changes, existing_prompt)
        diff = PromptDiff(list(set(modified_segments)), changes, plan.preserve_segments)

        return {
            "success": True,
            "modified_prompt": modified_prompt,
            "diff": diff.to_dict(),
            "lexical_correction_locality": locality,
            "editor_confidence": 0.95
        }


class RegressionProtection:
    """
    Ensures that targeted corrections do not cause unacceptable degradation in other dimensions.
    """
    def assess(self, prev_eval: dict, curr_eval: dict) -> dict:
        prev_scores = prev_eval.get("dimension_scores", {})
        curr_scores = curr_eval.get("dimension_scores", {})

        deltas = {}
        regressions = []
        is_acceptable = True

        for dim in prev_scores.keys():
            before = prev_scores[dim]
            after = curr_scores.get(dim, before)
            delta = after - before
            deltas[dim] = {
                "before": before,
                "after": after,
                "delta": delta
            }

            if delta < -0.10:
                regressions.append(dim)
                is_acceptable = False
            elif after < 0.60 and before >= 0.60:
                regressions.append(dim)
                is_acceptable = False

        return {
            "is_acceptable": is_acceptable,
            "deltas": deltas,
            "regressions": regressions
        }


class EscalationMetadata(str):
    """
    Escalation level string with attached provisional mechanism and run evaluation details.
    """
    def __new__(cls, level, mechanism, evaluation_confidence, failure_severity, improvement_delta):
        obj = str.__new__(cls, level)
        obj.level = level
        obj.mechanism = mechanism
        obj.evaluation_confidence = evaluation_confidence
        obj.failure_severity = failure_severity
        obj.improvement_delta = improvement_delta
        return obj


class RepeatedFailureDetector:
    """
    Tracks failure history across attempts, manages regeneration budget,
    and escalates to decision or intelligence gap levels on repeated failures.
    NOTE: The current attempt-based mechanism is explicitly marked as PROVISIONAL.
    """
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts
        self.attempts = []

    def record_attempt(self, plan: CorrectionPlan, evaluation_result: dict):
        self.attempts.append({
            "plan": plan.to_dict(),
            "result": evaluation_result
        })

    def check_escalation(self, current_dim: str, evaluation_result: dict = None, prev_evaluation_result: dict = None) -> EscalationMetadata:
        # Count failures in the same dimension
        dim_failures = [att for att in self.attempts if att["result"]["dimension_scores"].get(current_dim, 1.0) < 0.6]
        
        if len(dim_failures) >= self.max_attempts:
            level = "INTELLIGENCE"
        elif len(dim_failures) >= 2:
            level = "DECISION"
        else:
            level = "PROMPT"

        mechanism = "provisional_attempt_based"
        
        # Extract metadata metrics
        latest_eval = evaluation_result or (self.attempts[-1]["result"] if self.attempts else {})
        prev_eval = prev_evaluation_result or (self.attempts[-2]["result"] if len(self.attempts) > 1 else {})
        
        confidence = latest_eval.get("confidence", 1.0)
        
        severity = "HARD"
        if self.attempts:
            severity = self.attempts[-1]["plan"].get("failure", {}).get("severity", "HARD")
            
        curr_score = latest_eval.get("dimension_scores", {}).get(current_dim, 0.0)
        prev_score = prev_eval.get("dimension_scores", {}).get(current_dim, curr_score)
        delta = curr_score - prev_score
        
        return EscalationMetadata(level, mechanism, confidence, severity, delta)

    def generate_gap_report(self, current_dim: str, hypothesis: str) -> dict:
        report = IntelligenceGapReport(
            report_id=f"GAP-{int(time.time())}",
            failure_pattern=f"Repeated low score in dimension: '{current_dim}'",
            target_dimension=current_dim,
            attempts_count=len(self.attempts),
            gap_hypothesis=hypothesis
        )
        return report.to_dict()
