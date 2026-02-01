

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

    def advanceState(self, nextState: str) -> None:
        """
        Advance the session to the next deterministic state.

        Validation of allowed transitions must be enforced according
        to the predefined state flow in the capstone design.

        Args:
            nextState: The next state identifier.
        """
        # Transition validation belongs here once states are confirmed.
        self.currentState = nextState

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