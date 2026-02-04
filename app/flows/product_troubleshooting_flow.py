"""
ProductTroubleshootingFlow

Product-specific specialization of TroubleshootingFlow.
"""

from typing import Optional

from app.flows.troubleshooting_flow import TroubleshootingFlow


class ProductTroubleshootingFlow(TroubleshootingFlow):
    """
    Specializes step retrieval behavior by product/problem context.
    """

    def getNextStep(self, product: str, problem: str, stepIndex: int) -> Optional[str]:
        if product not in self.knowledgeBase:
            return None
        return super().getNextStep(product, problem, stepIndex)

