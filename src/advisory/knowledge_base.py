# =============================================
#              MODULE IMPORTS
# =============================================

from dataclasses import dataclass

# =============================================
#              KNOWLEDGE BASE
# =============================================
# Structured knowledge base for the operator-advisory feature.
# Every entry is a PARAPHRASE of real source material (CBIP manuals, CEA/CERC
# regulations, IS standards, an OEM O&M manual) -- not verbatim reproduction.
# Each entry is tagged (asset_type, fault_class) matching config.py's class_names,
# so retrieval is a deterministic dictionary lookup -- no embeddings needed.
# fault_class=None entries are asset-general guidance shown regardless of
# which fault is predicted. Every entry keeps its source_doc and source_section
# so any brief traces to where it came from.


@dataclass
class KnowledgeEntry:
    asset_type: str
    fault_class: str | None  # None = general guidance, shown for any fault_class
    title: str
    text: str
    source_doc: str
    source_section: str


KNOWLEDGE_BASE: list[KnowledgeEntry] = [

    # =========================================================================
    # TRANSFORMER
    # =========================================================================
    KnowledgeEntry(
        asset_type="transformer", fault_class=None,
        title="DGA escalation tiers",
        text="Compare the current DGA reading against the transformer's own prior samples, not just "
             "absolute limits. A reading within typical values needs no action beyond the normal sampling "
             "interval. A reading above typical values but not yet at alarm level should trigger increased "
             "sampling frequency to establish a trend. Only once concentrations or their rate of rise cross "
             "alarm thresholds should inspection or repair be considered.",
        source_doc="CBIP Manual on Transformers (Pub. 295)",
        source_section="DGA interpretation flowchart (IEC 60599-based)",
    ),
    KnowledgeEntry(
        asset_type="transformer", fault_class=None,
        title="Gas generation rate threshold",
        text="A sustained gas generation rate above roughly 100 ppm/day is an accepted general guideline "
             "for considering removal of a transformer from service, independent of the absolute concentration "
             "reached -- a fast rate of rise is itself a warning sign, not just the final level.",
        source_doc="CBIP Manual on Transformers (Pub. 295)",
        source_section="Trend analysis / gassing rate guidelines",
    ),
    KnowledgeEntry(
        asset_type="transformer", fault_class="D1 - Low Energy Discharge",
        title="Low-energy discharge response",
        text="A low-energy discharge signature (acetylene present but at low ratio to ethylene) warrants "
             "confirmatory oil sampling and a Duval Triangle cross-check before scheduling intrusive work -- "
             "this fault class does not on its own justify an unplanned outage.",
        source_doc="CBIP Manual on Transformers (Pub. 295)",
        source_section="IEC 60599 ratio-based fault table",
    ),
    KnowledgeEntry(
        asset_type="transformer", fault_class="D2 - High Energy Discharge",
        title="High-energy arcing response",
        text="High-energy discharge (acetylene dominant) is the single most critical DGA signature -- it is "
             "associated with internal arcing capable of catastrophic failure with little further warning. "
             "This class warrants an immediate shutdown evaluation, not routine trend monitoring.",
        source_doc="CBIP Manual on Transformers (Pub. 295)",
        source_section="Key gas criterion (IEEE C57.104-based)",
    ),
    KnowledgeEntry(
        asset_type="transformer", fault_class="T1 - Thermal Fault (<300C)",
        title="Low-temperature thermal fault",
        text="A thermal fault below 300°C is typically associated with methane and ethane generation from "
             "localized overheating. Increase sampling frequency and check cooling system performance and "
             "loading history before assuming a winding-level problem.",
        source_doc="CBIP Manual on Transformers (Pub. 295)",
        source_section="Relationship of evolved gases with temperature",
    ),
    KnowledgeEntry(
        asset_type="transformer", fault_class="T2 - Thermal Fault (300-700C)",
        title="Mid-temperature thermal fault",
        text="A thermal fault in the 300-700°C range is a significant escalation from T1 -- schedule a cooling "
             "system inspection and an oil-quality check (dielectric strength, moisture) within the next "
             "maintenance window rather than waiting for the next scheduled yearly test.",
        source_doc="CBIP Manual on Transformers (Pub. 295)",
        source_section="IEC 60599 ratio-based fault table",
    ),
    KnowledgeEntry(
        asset_type="transformer", fault_class="T3 - Thermal Fault (>700C)",
        title="Severe thermal fault",
        text="A thermal fault above 700°C indicates severe localized overheating and is associated with a rising "
             "ethylene/methane signature. This warrants a full internal inspection -- comparable in urgency to "
             "a high-energy discharge finding, since sustained temperatures at this level accelerate cellulose "
             "insulation degradation irreversibly.",
        source_doc="CBIP Manual on Transformers (Pub. 295)",
        source_section="Relationship of evolved gases with temperature",
    ),
    KnowledgeEntry(
        asset_type="transformer", fault_class="Partial Discharge",
        title="Partial discharge response",
        text="Partial discharge (corona) shows as hydrogen and methane with only minor other hydrocarbons. "
             "This is often an early-stage finding -- confirm with a repeat sample before escalating, since "
             "isolated partial discharge readings are less immediately dangerous than an arcing signature.",
        source_doc="CBIP Manual on Transformers (Pub. 295)",
        source_section="Associated faults with different fault gases",
    ),
    KnowledgeEntry(
        asset_type="transformer", fault_class=None,
        title="Post-protection-trip verification",
        text="After any protection trip attributed to an internal transformer fault, compare winding "
             "resistance, tan-delta, magnetizing current, and magnetic balance against the transformer's own "
             "pre-commissioning baseline. If results deviate significantly, escalate to specialized diagnostics "
             "(FRA, RVM, or partial-discharge testing) in consultation with the manufacturer before "
             "re-energizing.",
        source_doc="CBIP Manual on Transformers (Pub. 295)",
        source_section="Post-fault/post-maintenance test schedule",
    ),

    # =========================================================================
    # GENERATOR
    # =========================================================================
    KnowledgeEntry(
        asset_type="generator", fault_class=None,
        title="Vibration severity reference (Indian Standard)",
        text="IS 12075 sets vibration severity limits by shaft height and speed for Grade N (normal) rotating "
             "machines -- typically 1.8 mm/s RMS up to 1500 rpm, rising to 4.5 mm/s for larger shaft heights at "
             "higher speeds. A reading materially above the Grade N limit for the machine's own shaft height and "
             "speed range is grounds for closer inspection, independent of any single fixed threshold.",
        source_doc="IS 12075:2008",
        source_section="Table 1 -- Limits of Vibration Severity (Velocity Mode)",
    ),
    KnowledgeEntry(
        asset_type="generator", fault_class="Moderate Fault",
        title="Bearing overheating -- initial checks",
        text="Bearing temperature climbing above roughly 80°C, with or without unusual noise, is most commonly "
             "traced to set misalignment or a bearing working loose in its end-shield housing. Check alignment "
             "before assuming a bearing replacement is needed.",
        source_doc="Crompton Greaves AL-Series Alternator O&M Manual",
        source_section="8.8 Possible Faults -- Overheating, Noise and Vibration",
    ),
    KnowledgeEntry(
        asset_type="generator", fault_class="Severe Fault",
        title="Excessive vibration -- mechanical causes",
        text="Excessive vibration with humming noise that persists through a no-load start-up points to a "
             "faulty stator winding, not just mounting or coupling wear -- if defective mounting/coupling play "
             "has already been ruled out, plan for a stator winding inspection.",
        source_doc="Crompton Greaves AL-Series Alternator O&M Manual",
        source_section="8.8 Possible Faults -- Overheating, Noise and Vibration",
    ),
    KnowledgeEntry(
        asset_type="generator", fault_class="Thermal Warning",
        title="Frame overheating -- operating causes",
        text="Overheating of the alternator frame (as opposed to bearings specifically) is most often caused by "
             "blocked air inlets/outlets, operation above rated voltage, overloading, or a load power factor "
             "below 0.8 lagging -- check operating conditions before escalating to a winding-level investigation.",
        source_doc="Crompton Greaves AL-Series Alternator O&M Manual",
        source_section="8.8 Possible Faults -- Overheating, Noise and Vibration",
    ),
    KnowledgeEntry(
        asset_type="generator", fault_class="Thermal Runaway",
        title="Thermal runaway -- immediate action",
        text="Smoke, sparking, or flame from the alternator -- the end state of an uncontrolled thermal "
             "trajectory -- calls for immediately stopping the set, not further diagnosis in service. Root cause "
             "is typically a short circuit in the external circuit or in wiring between the alternator and "
             "control board.",
        source_doc="Crompton Greaves AL-Series Alternator O&M Manual",
        source_section="8.8 Possible Faults -- Overheating, Noise and Vibration",
    ),
    KnowledgeEntry(
        asset_type="generator", fault_class=None,
        title="Grid Disturbance severity context",
        text="If this generator's condition leads to (or follows) an unplanned trip, CEA Grid Standards classify "
             "the resulting event by how much antecedent generation or load was lost: under 10% is GD-1, "
             "10-20% is GD-2, 20-30% is GD-3, 30-40% is GD-4, and 40% or more is GD-5 -- the most severe "
             "category. This gives a standardized severity scale for how a single generator's failure maps to "
             "grid-level impact.",
        source_doc="CEA Grid Standards Regulations, 2010",
        source_section="Categorisation of Grid Incidents and Grid Disturbance",
    ),

    # =========================================================================
    # CIRCUIT BREAKER
    # =========================================================================
    KnowledgeEntry(
        asset_type="circuit_breaker", fault_class=None,
        title="Breaker failure is rare but must be assumed possible",
        text="Breaker failure occurs in roughly 0.01% of normal switching operations and 0.1% of fault-clearance "
             "operations -- rare, but the consequence of an undetected failure (loss of a much larger section of "
             "network via backup breakers) is severe enough that breaker-fail (LBB) protection must remain "
             "continuously in service, never treated as optional redundancy.",
        source_doc="CBIP Manual on Reliable Fault Clearance and Back-up Protection of EHV and UHV Networks",
        source_section="Chapter 10 -- Switching Devices",
    ),
    KnowledgeEntry(
        asset_type="circuit_breaker", fault_class="Mechanical Jamming - Mild",
        title="Contact travel time increasing",
        text="A gradually increasing contact travel time against nameplate specification points to drying or "
             "degraded lubrication, worn linkages, or a weakening trip spring in the operating mechanism -- "
             "schedule mechanism lubrication and inspection before travel time reaches a level that risks a "
             "failure-to-trip event.",
        source_doc="CBIP Manual on Reliable Fault Clearance and Back-up Protection of EHV and UHV Networks",
        source_section="Chapter 10 -- Switching Devices / IEC 62271-100 context",
    ),
    KnowledgeEntry(
        asset_type="circuit_breaker", fault_class="Mechanical Jamming - Severe",
        title="Severe jamming -- treat as a failure-to-trip risk",
        text="Once contact travel time is far outside its reference value, the practical risk is a genuine "
             "failure to interrupt fault current on demand -- the same condition breaker-fail (LBB) protection "
             "exists to back up. This should be treated with the same urgency as any other single point of "
             "failure in the protection scheme: inspect and, where indicated, take the breaker out of service "
             "for the affected element rather than waiting for the next scheduled outage.",
        source_doc="CBIP Manual on Reliable Fault Clearance and Back-up Protection of EHV and UHV Networks",
        source_section="10.5 Breaker Failure Protection -- Basic Principle",
    ),
    KnowledgeEntry(
        asset_type="circuit_breaker", fault_class="Coil Degradation - Early",
        title="Trip coil current drift",
        text="An elevated trip coil RMS current can indicate a developing partial short circuit in the coil "
             "winding (insulation breakdown between turns), while a reduced peak current suggests an open "
             "circuit developing -- either direction of drift from baseline is worth a coil resistance check at "
             "the next opportunity, not just when the coil fails outright.",
        source_doc="CBIP Manual on Reliable Fault Clearance and Back-up Protection of EHV and UHV Networks",
        source_section="Chapter 10 -- Switching Devices (trip coil signature context)",
    ),
    KnowledgeEntry(
        asset_type="circuit_breaker", fault_class="Coil Degradation - Severe",
        title="Trip coil -- escalated risk",
        text="Severe trip coil degradation is functionally the same hazard breaker-fail protection is designed "
             "to catch -- a coil that cannot reliably release the mechanism latch on command. Utilities are "
             "advised to keep breaker performance data on record specifically to plan interventions like this "
             "before an actual failure-to-trip event occurs.",
        source_doc="CBIP Manual on Reliable Fault Clearance and Back-up Protection of EHV and UHV Networks",
        source_section="10.10 Recommendations for Use of Breaker Fail Protection",
    ),

    # =========================================================================
    # RELAY
    # =========================================================================
    KnowledgeEntry(
        asset_type="relay", fault_class=None,
        title="Backup protection philosophy",
        text="Backup protection exists specifically because main protection or the primary breaker sometimes "
             "fails to clear a fault -- ideal backup should be as independent of the main protection as "
             "practical (separate current/voltage inputs, separate DC supply, separate trip coil) so a single "
             "shared weakness cannot defeat both layers at once.",
        source_doc="CBIP Manual on Reliable Fault Clearance and Back-up Protection of EHV and UHV Networks",
        source_section="2.2/2.3 Back-up Protection / Remote Back-up Protection",
    ),
    KnowledgeEntry(
        asset_type="relay", fault_class="Elevated Fault Current",
        title="Elevated fault current -- verify before escalating",
        text="A rise in measured fault current alone, without a corresponding drop in apparent impedance into "
             "the trip zone, can reflect a genuine but distant fault or a measurement/CT issue rather than "
             "relay degradation -- cross-check against the impedance trend before concluding the relay itself "
             "needs attention.",
        source_doc="CBIP Manual on Reliable Fault Clearance and Back-up Protection of EHV and UHV Networks",
        source_section="General protection coordination principles",
    ),
    KnowledgeEntry(
        asset_type="relay", fault_class="Moderate Impedance Fault",
        title="Impedance trending into the trip zone",
        text="Apparent impedance falling toward the boundary of the relay's mho characteristic indicates the "
             "measured fault is moving electrically closer to the relay -- confirm protection coordination with "
             "adjacent zones (selectivity) is still intact for this condition, per standard distance-protection "
             "coordination practice.",
        source_doc="CBIP Manual on Reliable Fault Clearance and Back-up Protection of EHV and UHV Networks",
        source_section="4.1.2.2 Selectivity (protection coordination)",
    ),
    KnowledgeEntry(
        asset_type="relay", fault_class="Critical Zone Fault",
        title="Fault deep in the trip zone",
        text="An apparent impedance reading deep inside the trip zone (lowest end of the observed range) should "
             "be treated as an imminent-trip condition -- verify breaker-fail (LBB) backup is armed and "
             "functioning for this relay's associated breaker, since this is exactly the condition where a "
             "stuck breaker following a correct trip command would otherwise go undetected the longest.",
        source_doc="CBIP Manual on Reliable Fault Clearance and Back-up Protection of EHV and UHV Networks",
        source_section="10.5.1 Breaker Failure Protection -- Basic Principle",
    ),

    # =========================================================================
    # IS 10118 (Part IV) -- switchgear/control gear maintenance code of practice
    # =========================================================================
    KnowledgeEntry(
        asset_type="circuit_breaker", fault_class=None,
        title="Routine operation prevents stiffness-related failure to trip",
        text="A breaker that isn't periodically operated can fail to trip on a real fault due to mechanism "
             "stiffness or trip-circuit defects developing unnoticed. Every automatic circuit breaker should be "
             "tripped and reclosed at least once every six months specifically to guard against this -- exercising "
             "a breaker via manual trip/close (as this dashboard's switchgear controls do) is itself a "
             "maintenance action, not just a test.",
        source_doc="IS 10118 (Part IV):1982, Reaffirmed 2001",
        source_section="4.2 / 5.2 Routine Operation of Circuit-Breakers",
    ),
    KnowledgeEntry(
        asset_type="circuit_breaker", fault_class=None,
        title="Post-fault-operation overhaul",
        text="After any operation under actual fault conditions, a complete inspection and overhaul should follow "
             "as soon as practical -- contacts and arc-control devices checked for burning/damage, mechanism "
             "checked for correct operation, and an insulation resistance test made before the breaker is "
             "returned to service. This is a stricter standard than routine inspection because breaking-capacity "
             "and insulation level need to be confirmed restored, not just contact wear.",
        source_doc="IS 10118 (Part IV):1982, Reaffirmed 2001",
        source_section="4.4 Maintenance After Operation Under Fault Conditions",
    ),
    KnowledgeEntry(
        asset_type="relay", fault_class=None,
        title="Trend insulation resistance readings, not single values",
        text="Insulation resistance on relay/control circuits is best judged by comparing readings taken over a "
             "considerable period, not a single measurement -- a steady decline is a greater warning sign than a "
             "steady low value, since the trend indicates active degradation while a stable low value may simply "
             "be that circuit's normal baseline.",
        source_doc="IS 10118 (Part IV):1982, Reaffirmed 2001",
        source_section="8.2.7 Maintenance of Insulation",
    ),
    KnowledgeEntry(
        asset_type="relay", fault_class=None,
        title="CT secondary safety when disconnecting a relay",
        text="Where a relay is fed from a current transformer, its CT secondary must be short-circuited before "
             "the relay is disconnected -- an open CT secondary is a shock and equipment-damage hazard, not just "
             "a data-loss inconvenience. This applies whenever a relay is pulled for testing or replacement "
             "following a fault-classification alert, not only during scheduled maintenance.",
        source_doc="IS 10118 (Part IV):1982, Reaffirmed 2001",
        source_section="8.2.6.4",
    ),
]


def get_entries(asset_type: str, fault_class: str | None = None) -> list[KnowledgeEntry]:
    """Returns every general (fault_class=None) entry for this asset PLUS
    any entries specific to the given fault_class, general entries first."""
    general = [e for e in KNOWLEDGE_BASE if e.asset_type == asset_type and e.fault_class is None]
    specific = [e for e in KNOWLEDGE_BASE if e.asset_type == asset_type and e.fault_class == fault_class]
    return general + specific