"""
TroubleshootingStep

Passive data structure representing a single troubleshooting step within
an ordered troubleshooting flow. This class stores step metadata only and
contains no sequencing, validation, or decision logic.

All flow control, evaluation, and state transitions are handled by
TroubleshootingFlow and related reasoning components.
"""

from typing import Optional


class TroubleshootingStep:
    """
    Represents a single step in a troubleshooting sequence.

    This object is intentionally passive and exists only to hold structured
    data referenced during troubleshooting.
    """

    def __init__(
        self,
        stepId: str,
        instruction: str,
        expectedOutcome: str,
        nextStepId: Optional[str] = None,
        isTerminal: bool = False
    ):
        # Unique identifier for this troubleshooting step
        self.stepId = stepId

        # Instruction or action presented to the agent
        self.instruction = instruction

        # Description of the expected successful outcome
        self.expectedOutcome = expectedOutcome

        # Identifier of the next step if this step does not resolve the issue
        # Stored only. Sequencing logic exists outside this class.
        self.nextStepId = nextStepId

        # Indicates whether this step ends the troubleshooting flow
        self.isTerminal = isTerminal
