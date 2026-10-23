# =============================================
#              MODULE IMPORTS
# =============================================

from dataclasses import dataclass

from src.advisory.retriever import retrieve

# =============================================
#              BRIEF GENERATOR
# =============================================
# Turns (classification, forecast, retrieved knowledge) into a short operator
# brief. This is TEMPLATE-FILL ONLY -- it selects and formats real retrieved
# passages; it generates no new sentences.
#
# NOTE: An LLM asked to "write guidance" for real infrastructure can hallucinate
# a plausible-sounding but wrong instruction -- a failure mode worse than a
# wrong classification, because it reads as confident prose someone might act on.
# Every sentence in this module's output traces to a KnowledgeEntry with a real
# source_doc/source_section. If a constrained single-shot rephrasing layer is
# ever added, it must be restricted to rephrasing THESE retrieved passages only --
# never asked to reason freely about what action to take.


@dataclass
class OperatorBrief:
    asset_type: str
    fault_class: str
    confidence: float
    forecast_line: str | None
    sections: list[dict]  # [{"title": ..., "text": ..., "source": ...}]
    markdown: str


def build_brief(asset_type: str, classification: dict, forecast: dict | None) -> OperatorBrief:
    """
    classification: {fault_code, fault_label, confidence} -- from AssetHealthPredictor.classify()
    forecast: {value, target_name, higher_is_worse} or None -- from AssetHealthPredictor.forecast()
    """
    fault_class = classification["fault_label"]
    confidence = classification["confidence"]
    entries = retrieve(asset_type, fault_class)

    forecast_line = None
    if forecast is not None:
        direction = "rising" if forecast["higher_is_worse"] else "falling"
        forecast_line = f"Forecast: {forecast['target_name']} trending {direction} (predicted next value: {forecast['value']:.2f})."

    sections = [
        {"title": e.title, "text": e.text, "source": f"{e.source_doc} -- {e.source_section}"}
        for e in entries
    ]

    md_lines = [f"**Predicted state: {fault_class}** (model confidence {confidence:.0%})"]
    if forecast_line:
        md_lines.append(forecast_line)
    md_lines.append("")

    if sections:
        for s in sections:
            md_lines.append(f"**{s['title']}**")
            md_lines.append(s["text"])
            md_lines.append(f"*Source: {s['source']}*")
            md_lines.append("")
    else:
        md_lines.append("_No specific guidance on file for this fault class yet._")

    return OperatorBrief(
        asset_type=asset_type,
        fault_class=fault_class,
        confidence=confidence,
        forecast_line=forecast_line,
        sections=sections,
        markdown="\n".join(md_lines),
    )