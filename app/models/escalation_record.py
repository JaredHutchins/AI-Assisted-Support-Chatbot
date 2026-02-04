"""
EscalationRecord

Passive data structure representing escalation output prepared when
troubleshooting does not resolve the issue at Tier 1.
"""


class EscalationRecord:
    """
    Holds escalation summary fields only.

    This object intentionally contains no workflow logic.
    """

    def __init__(self, summary: str, escalationReason: str):
        self.summary = summary
        self.escalationReason = escalationReason

