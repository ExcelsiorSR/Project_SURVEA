# =============================================
#              MODULE IMPORTS
# =============================================

from src.advisory.knowledge_base import get_entries, KnowledgeEntry

# =============================================
#              ADVISORY RETRIEVER
# =============================================
# Exact-tag lookup -- deliberately NOT embedding-based.
# With ~5-10 knowledge base entries per (asset_type, fault_class) bucket,
# exact-tag lookup already IS the correct retrieval -- no ranking ambiguity
# to resolve with semantic similarity. Adding sentence-transformers would
# add ~80MB RAM on every deploy for zero retrieval-quality benefit.
# Revisit this if the knowledge base grows into hundreds of entries with
# fuzzy/overlapping tags -- not before.


def retrieve(asset_type: str, fault_class: str) -> list[KnowledgeEntry]:
    """Returns the general + fault-specific knowledge entries for one
    asset/fault-class pair. Never raises -- an unknown combination just
    returns the general entries alone (which always exist per asset),
    so the brief still renders sensibly."""
    return get_entries(asset_type, fault_class)