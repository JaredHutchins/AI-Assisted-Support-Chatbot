

"""
Core session context for the ASC.

This module contains deterministic, framework-agnostic session state handling.
It deliberately avoids Flask imports, HTTP concerns, or UI assumptions.

Authoritative note:
- Valid states, transitions, and resolution or escalation criteria
  must align with existing capstone design documents and UML.
- Do not introduce new states or flows here without confirming against
  those artifacts first.
"""


class SessionContext:
    """
    Represents a single support session.

    This class is intentionally minimal. It stores session state and
    exposes deterministic decision points without embedding transport
    or presentation logic.
    """

    # Allowed state transitions based strictly on the UML state machine.
    # Keys represent the current state.
    # Values represent the set of valid next states.
    _allowedTransitions = {
        "Idle": {"IssueCapture"},
        "IssueCapture": {"KnowledgeRetrieval"},
        "KnowledgeRetrieval": {
            "KnowledgeRetrieval",  # Explicit self-loop
            "ResolutionDelivered",
            "EscalationPrepared",
        },
        "ResolutionDelivered": {"SessionComplete"},
        "EscalationPrepared": {"SessionComplete"},
        "SessionComplete": set(),
    }

    def __init__(self, sessionId: str):
        """
        Initialize a new session context.

        Args:
            sessionId: Unique identifier for the support session.
        """
        self.sessionId = sessionId

        # Current logical state of the session.
        # The concrete state values must come from existing design artifacts.
        self.currentState = None

        # Terminal outcome flags.
        self.isResolved = False
        self.isEscalated = False

    def advanceState(self, nextState: str) -> bool:
        """
        Attempt to advance the session to the next deterministic state.

        The transition is validated against the UML-defined state machine.
        Invalid transitions are rejected without raising exceptions.

        Args:
            nextState: The requested next state identifier.

        Returns:
            True if the transition succeeded, otherwise False.
        """
        # Terminal sessions cannot transition further.
        if self.isTerminal():
            return False

        # Initial state must be set explicitly from Idle.
        if self.currentState is None:
            if nextState != "Idle":
                return False
            self.currentState = "Idle"
            return True

        allowedNextStates = self._allowedTransitions.get(self.currentState, set())

        if nextState not in allowedNextStates:
            return False

        self.currentState = nextState
        return True

    def markResolved(self) -> None:
        """
        Mark the session as successfully resolved.

        Once resolved, no further state transitions should occur.
        """
        self.isResolved = True
        self.isEscalated = False

    def markEscalated(self) -> None:
        """
        Mark the session as escalated to a higher support tier.

        Escalation is terminal and mutually exclusive with resolution.
        """
        self.isEscalated = True
        self.isResolved = False

    def isTerminal(self) -> bool:
        """
        Check whether the session has reached a terminal outcome.

        Returns:
            True if resolved or escalated, otherwise False.
        """
        return self.isResolved or self.isEscalated