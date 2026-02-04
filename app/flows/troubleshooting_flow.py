"""
TroubleshootingFlow

Shared reasoning component for retrieving article steps and validating
step progression.
"""

from typing import Dict, List, Optional

from app.models.escalation_record import EscalationRecord


class TroubleshootingFlow:
    """
    Base reasoning flow for deterministic troubleshooting.
    """

    def __init__(self, knowledgeBase: Dict[str, Dict[str, List[str]]]):
        self.knowledgeBase = knowledgeBase

    def retrieveArticle(self, product: str, problem: str) -> List[str]:
        """
        Return all troubleshooting steps for a product/problem pair.
        """
        return list(self.knowledgeBase.get(product, {}).get(problem, []))

    def validateStep(self, steps: List[str], stepIndex: int) -> bool:
        """
        Validate that a step index points to an available troubleshooting step.
        """
        return 0 <= stepIndex < len(steps)

    def getNextStep(self, product: str, problem: str, stepIndex: int) -> Optional[str]:
        """
        Return the next troubleshooting step, or None when exhausted/invalid.
        """
        steps = self.retrieveArticle(product, problem)
        if not self.validateStep(steps, stepIndex):
            return None
        return steps[stepIndex]

    def prepareEscalation(
        self,
        product: str,
        problem: str,
        attemptedSteps: List[str]
    ) -> EscalationRecord:
        """
        Build a structured escalation record from current troubleshooting data.
        """
        summary = (
            f"Product: {product}; Problem: {problem}; "
            f"Attempted Steps: {', '.join(attemptedSteps) if attemptedSteps else 'None'}"
        )
        return EscalationRecord(
            summary=summary,
            escalationReason="All standard troubleshooting steps exhausted"
        )

