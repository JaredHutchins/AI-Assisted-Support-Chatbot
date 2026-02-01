"""
KnowledgeArticle

Passive data structure representing a single knowledge article used during
knowledge retrieval. This class stores article metadata only and contains
no control logic, sequencing, validation, or session awareness.

All decision-making, selection, and applicability checks are handled by
reasoning components elsewhere in the system.
"""

from typing import List, Optional


class KnowledgeArticle:
    """
    Represents a single knowledge article.

    This object is intentionally passive. It exists only to hold structured
    data that is referenced during troubleshooting and knowledge retrieval.
    """

    def __init__(
        self,
        articleId: str,
        title: str,
        prerequisites: Optional[List[str]] = None
    ):
        # Unique identifier for the knowledge article
        self.articleId = articleId

        # Human-readable title presented to the agent
        self.title = title

        # List of prerequisite conditions required for applicability
        # Stored only. Evaluation occurs outside this class.
        self.prerequisites = prerequisites or []
