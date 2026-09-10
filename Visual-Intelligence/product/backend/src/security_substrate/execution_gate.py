"""
IF-EXECUTE-001 ExecutionGate implementation.
Fail-closed pass-through lock enforcing state check. Zero policy authority.
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional

from .epistemic_state import EpistemicState
from .assurance_loop import AssuranceLoopController
from .exceptions import ExecutionGateLockedException, FailClosedException


@dataclass
class GateResponse:
    """
    Response object returned by ExecutionGate.
    """
    permitted: bool
    reason: str
    execution_output: Optional[Any] = None


class ExecutionGate:
    """
    IF-EXECUTE-001 Pass-Through Lock.
    Permits action execution ONLY if Active EpistemicState is VERIFIED.
    Default state is PERMITTED = False.
    """
    def __init__(self, controller: AssuranceLoopController):
        if not controller or not isinstance(controller, AssuranceLoopController):
            raise FailClosedException("ExecutionGate requires a valid AssuranceLoopController instance.")
        self.controller = controller

    def is_permitted(self) -> bool:
        """Helper to query if gate is currently unlocked."""
        return self.controller.get_current_state() == EpistemicState.VERIFIED

    def request_execution(
        self,
        payload_action: Any,
        callable_func: Optional[Callable] = None,
        *args,
        **kwargs
    ) -> GateResponse:
        """
        IF-EXECUTE-001 Interface Method: Requests gate execution for payload_action.

        Returns:
            GateResponse with permitted=True ONLY if state is VERIFIED.
        """
        active_state = self.controller.get_current_state()

        if active_state != EpistemicState.VERIFIED:
            return GateResponse(
                permitted=False,
                reason=f"Execution BLOCKED: Active epistemic state is {active_state.value} (requires VERIFIED).",
                execution_output=None
            )

        if callable_func is not None:
            try:
                output = callable_func(*args, **kwargs)
                return GateResponse(
                    permitted=True,
                    reason="Execution PERMITTED: Epistemic state is VERIFIED.",
                    execution_output=output
                )
            except Exception as e:
                # Execution failure inside permitted closure raises FailClosedException
                raise FailClosedException(f"Execution payload failed inside ExecutionGate: {str(e)}") from e

        return GateResponse(
            permitted=True,
            reason="Execution PERMITTED: Epistemic state is VERIFIED.",
            execution_output=None
        )

    def execute_or_raise(self, payload_action: Any, callable_func: Callable, *args, **kwargs) -> Any:
        """
        Executes payload_action if VERIFIED, or raises ExecutionGateLockedException if locked.
        """
        response = self.request_execution(payload_action, callable_func, *args, **kwargs)
        if not response.permitted:
            raise ExecutionGateLockedException(response.reason)
        return response.execution_output
