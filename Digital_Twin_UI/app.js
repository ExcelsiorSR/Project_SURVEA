/* ============================================================
   Digital Twin Interface -- Shared Dashboard Logic
   Expects window.GRID_ID to be set ('39' or '118') by the page
   that includes this script, before this file runs.

   NOTE: Agent Copilot lives in ai_dashboard.html / ai_app.js now,
   not here. This file is the Digital Twin only -- it has no idea
   the AI Architecture service exists, matching the same clean
   separation the backend already enforces.
   ============================================================ */

const GRID_ID = window.GRID_ID;
const API_URL = "http://127.0.0.1:8001";     // Digital Twin service only

let cy = null;
let selectedBus = null;
let latestGridState = null;

// ------------------------------------------------------------
// ICONS -- generator/transformer buses ALWAYS get their correct
// icon (from /topology's node_type field); only genuine load
// buses get a randomized consumer icon for visual variety.
// ------------------------------------------------------------
const LOAD_ICONS = [
  "icons/factory.png", "icons/home.png", "icons/sky-scrappers.png",
  "icons/school.png", "icons/college.png", "icons/gas-station.png",
  "icons/hospital.png", "icons/museum.png", "icons/office.png",
  "icons/banks.png", "icons/post-office.png", "icons/shop.png",
  "icons/shopping-mall.png",
];

function iconForNode(nodeType) {
  switch (nodeType) {
    case "GENERATOR": return "icons/power-plant.png";
    case "TRANSFORMER": return "icons/transformer.png";
    case "LOAD": return LOAD_ICONS[Math.floor(Math.random() * LOAD_ICONS.length)];
    default: return "icons/transformer.png"; // JUNCTION
  }
}

// ------------------------------------------------------------
// CYTOSCAPE GRAPH
// ------------------------------------------------------------
async function loadTopology() {
  const res = await fetch(`${API_URL}/topology?grid=${GRID_ID}`);
  const data = await res.json();
  if (!data || !data.nodes || !data.edges) return;

  const enrichedNodes = data.nodes.map(node => ({
    ...node,
    data: { ...node.data, image: iconForNode(node.data.node_type) }
  }));

  // --- EQUIPMENT SATELLITE NODES ---
  // Every generator/transformer/load bay has real substation equipment
  // around it (isolators, CTs, PTs, arrestors, wave traps) that isn't
  // simulated/aged like the 4 SURVEA asset classes -- it's decorative
  // single-line-diagram context, fetched on click from
  // /substation_equipment. One small "gear" satellite per non-JUNCTION bus,
  // linked to its parent by a thin dotted edge so cose layout settles it
  // right next to the asset it belongs to.
  const equipmentNodes = [];
  const equipmentEdges = [];
  data.nodes.forEach(node => {
    if (node.data.node_type === "JUNCTION") return;
    const busId = node.data.id;
    const eqId = `equip-${busId}`;
    equipmentNodes.push({ data: { id: eqId, parent_bus: busId, is_equipment: true } });
    equipmentEdges.push({ data: { id: `equip-edge-${busId}`, source: busId, target: eqId, is_equipment_link: true } });
  });

  cy = cytoscape({
    container: document.getElementById("cy"),
    elements: [...enrichedNodes, ...data.edges, ...equipmentNodes, ...equipmentEdges],
    layout: { name: "cose", animate: false },
    style: [
      {
        selector: "node",
        style: {
          "background-image": "data(image)",
          "background-fit": "cover",
          "background-color": "transparent",
          "label": "data(id)",
          "color": "#ffffff",
          "text-valign": "bottom",
          "text-margin-y": 5,
          "font-size": "12px",
          "width": 35,
          "height": 35
        }
      },
      {
        // Equipment satellite dot -- overrides the generic node style above
        // (later selectors win ties in cytoscape).
        selector: "node[?is_equipment]",
        style: {
          "background-image": "none",
          "background-color": "#1b2735",
          "label": "\u2699",
          "text-valign": "center",
          "text-halign": "center",
          "font-size": "10px",
          "color": "#00a8ff",
          "border-width": 1,
          "border-color": "#00a8ff",
          "border-opacity": 0.8,
          "width": 16,
          "height": 16
        }
      },
      {
        selector: "edge",
        style: {
          "width": 2,
          "line-color": "#444444",
          "curve-style": "bezier",
          "line-style": "dashed",
          "line-dash-pattern": [5, 5]
        }
      },
      {
        selector: "edge[?is_equipment_link]",
        style: {
          "width": 1,
          "line-color": "#2a2a2a",
          "curve-style": "straight",
          "line-style": "dotted",
          "target-arrow-shape": "none"
        }
      },
      {
        // CURRENTLY overloaded right now (>100% loading in live telemetry)
        selector: ".overloaded",
        style: {
          "line-color": "#e74c3c",
          "width": 5,
          "shadow-blur": 15,
          "shadow-color": "#e74c3c",
          "shadow-opacity": 0.9,
          "transition-property": "line-color, width",
          "transition-duration": "0.3s"
        }
      },
      {
        // WOULD become insecure if lost (N-1 contingency risk) -- distinct
        // amber color so it's visually different from an actual live
        // overload. Lower z-index priority than .overloaded if a line is
        // somehow both (cytoscape applies the later-defined style last).
        selector: ".contingency-risk",
        style: {
          "line-color": "#f39c12",
          "width": 4,
          "line-style": "dashed",
          "shadow-blur": 10,
          "shadow-color": "#f39c12",
          "shadow-opacity": 0.7
        }
      },
      {
        // Highest-demand facilities right now -- a gold glow, recomputed
        // every telemetry tick in renderTelemetry(). Any bus within 90% of
        // the current peak load lights up, not just a single "#1" bus, so
        // a genuine cluster of hotspots is visible together.
        selector: ".high-demand",
        style: {
          "border-width": 3,
          "border-color": "#ffd700",
          "border-opacity": 1,
          "shadow-blur": 25,
          "shadow-color": "#ffd700",
          "shadow-opacity": 0.9,
          "width": 42,
          "height": 42,
          "transition-property": "shadow-blur, shadow-opacity, width, height",
          "transition-duration": "0.4s"
        }
      },
      {
        // Visual state for a disconnected line
        selector: ".line-tripped",
        style: {
          "line-color": "#475569",
          "line-style": "dotted",
          "opacity": 0.3,
          "shadow-blur": 0
        }
      }
    ]
  });

  // --- LINE HOVER TOOLTIP ---
  const tooltip = document.getElementById("line-tooltip");

  cy.on("mouseover", "edge", (evt) => {
    const edge = evt.target;
    const lineId = edge.id().replace("line", "");
    const isTripped = edge.data("tripped") === true;
    
    // Extract telemetry (Defaults to 0 if the backend doesn't send line_metrics yet)
    const load = latestGridState?.line_metrics?.[lineId]?.loading_percent || 0;
    const current = latestGridState?.line_metrics?.[lineId]?.i_ka || 0;
    const pf = latestGridState?.line_metrics?.[lineId]?.pf || 1.0;

    const actionText = isTripped ? 
      '<span style="color:#4ade80;">Click to RESTORE this line</span>' : 
      '<span style="color:#f87171;">Click to TRIP this line</span>';

    // Circuit breaker dataset features (cb_refined_dataset.csv) -- every
    // line has exactly one breaker, keyed by the same line id.
    const cb = latestGridState?.asset_health?.circuit_breakers?.[lineId];
    const cbHtml = cb ? `
      <hr>
      <strong style="color:#fb923c;">Breaker ${lineId}</strong> &mdash; <span style="color:${cb.fault_class === 'Normal' ? '#4ade80' : '#f87171'};">${cb.fault_class}</span><br>
      Contact Travel: ${Number(cb.Contact_Travel_Time_ms).toFixed(1)} ms | TCCS Duration: ${Number(cb.TCCS_Duration_ms).toFixed(1)} ms<br>
      Contact Temp: ${Number(cb.Contact_Temperature_C).toFixed(1)}&deg;C | SF6 Pressure: ${Number(cb.Gas_Pressure_bar).toFixed(2)} bar
    ` : "";

    tooltip.innerHTML = `
      <strong style="color: var(--accent-cyan);">Line ${lineId}</strong><br>
      Status: ${isTripped ? 'TRIPPED' : 'ACTIVE'}<br>
      Loading: ${Number(load).toFixed(1)}%<br>
      Current: ${Number(current).toFixed(2)} kA<br>
      Power Factor: ${Number(pf).toFixed(3)}<br>
      ${cbHtml}
      <hr>
      ${actionText}
    `;
    tooltip.classList.remove("hidden");
  });

  cy.on("mousemove", "edge", (evt) => {
    // Make the HTML tooltip follow the Cytoscape rendered mouse position
    tooltip.style.left = `${evt.originalEvent.pageX}px`;
    tooltip.style.top = `${evt.originalEvent.pageY}px`;
  });

  cy.on("mouseout", "edge", () => {
    tooltip.classList.add("hidden");
  });

  // --- BUS/NODE HOVER TOOLTIP ---
  cy.on("mouseover", "node[!is_equipment]", (evt) => {
    const node = evt.target;
    const busId = node.id();
    const nodeType = node.data("node_type"); // GENERATOR, LOAD, or TRANSFORMER
    
    // Extract telemetry
    const v_pu = latestGridState?.bus_metrics?.[busId]?.v_pu || 0;
    const v_ang = latestGridState?.bus_metrics?.[busId]?.v_ang || 0;
    const load = latestGridState?.bus_loads?.[busId] || 0;

    // Relay dataset features (relay_dataset_F.csv) -- asset_health.relays is
    // keyed 1:1 by bus id already, so this bus's protection relay is right here.
    const relay = latestGridState?.asset_health?.relays?.[busId];
    const relayHtml = relay ? `
      <hr>
      <strong style="color:#a78bfa;">Relay ${busId}</strong> &mdash; <span style="color:${relay.fault_class === 'Normal' ? '#4ade80' : '#f87171'};">${relay.fault_class}</span><br>
      Impedance Z: ${Number(relay.Impedance_Z).toFixed(3)} &Omega;<br>
      I_rms: ${Number(relay.I_rms).toFixed(3)} | I_peak: ${Number(relay.I_peak).toFixed(3)}<br>
      V_rms: ${Number(relay.V_rms).toFixed(3)} | V_peak: ${Number(relay.V_peak).toFixed(3)}
    ` : "";

    tooltip.innerHTML = `
      <strong style="color: #fde047;">Bus ${busId} (${nodeType})</strong><br>
      Voltage: ${Number(v_pu).toFixed(3)} p.u.<br>
      Angle: ${Number(v_ang).toFixed(1)}&deg;<br>
      Live Load: ${Number(load).toFixed(2)} MW<br>
      ${relayHtml}
      <hr>
      <span style="color:#94a3b8;">Click to open Facility Control</span>
    `;
    tooltip.classList.remove("hidden");
  });

  // --- EQUIPMENT SATELLITE HOVER TOOLTIP ---
  cy.on("mouseover", "node[?is_equipment]", (evt) => {
    tooltip.innerHTML = `
      <strong style="color: var(--accent-cyan);">Substation Equipment</strong><br>
      <span style="color:#94a3b8;">Click to view CT/PT/isolator/arrestor bay</span>
    `;
    tooltip.classList.remove("hidden");
  });

  cy.on("mousemove", "node", (evt) => {
    tooltip.style.left = `${evt.originalEvent.pageX}px`;
    tooltip.style.top = `${evt.originalEvent.pageY}px`;
  });

  cy.on("mouseout", "node", () => {
    tooltip.classList.add("hidden");
  });

  // --- BI-DIRECTIONAL TRIP/RESTORE ---
  cy.on("tap", "edge", (evt) => {
    const edge = evt.target;
    const lineId = parseInt(edge.id().replace("line", ""), 10);
    const isTripped = edge.data("tripped") === true;

    if (isTripped) {
      // RESTORE LINE
      edge.data("tripped", false);
      edge.removeClass("line-tripped");
      fetch(`${API_URL}/restore_line/${GRID_ID}/${lineId}`, { method: "POST" })
        .catch(err => console.error(err));
    } else {
      // TRIP LINE
      edge.data("tripped", true);
      edge.addClass("line-tripped");
      fetch(`${API_URL}/inject_fault/${lineId}?grid=${GRID_ID}`, { method: "POST" })
        .catch(err => console.error(err));
    }
  });

  cy.on("tap", "node[!is_equipment]", (evt) => {
    const node = evt.target;
    const busId = node.id();
    const nodeType = node.data("node_type");
    const liveLoad = latestGridState?.bus_loads?.[busId] ?? node.data("load") ?? 0;
    selectedBus = busId;
    document.getElementById("targetFacility").textContent = `Facility ${busId}`;
    document.getElementById("currentLoad").textContent = `${Number(liveLoad).toFixed(2)} MW`;
    document.getElementById("loadInput").placeholder = `Current: ${Number(liveLoad).toFixed(2)} MW`;
    document.getElementById("loadInput").value = "";
    document.getElementById("loadCommandResult").textContent = "";
    // --- AUTO-POPULATE FAULT INJECTION CONSOLE ---
  const typeSelect = document.getElementById("degradeAssetType");
  const idInput = document.getElementById("degradeAssetId");
  
  if (typeSelect && idInput) {
    const genId = node.data("gen_id");
    const trafoId = node.data("trafo_id");

    if (nodeType === "GENERATOR" && genId !== null && genId !== undefined) {
      typeSelect.value = "generator";
      idInput.value = genId;
    } else if (nodeType === "TRANSFORMER" && trafoId !== null && trafoId !== undefined) {
      typeSelect.value = "transformer";
      idInput.value = trafoId;
    } else {
      // Fallback: every bus has a relay, so target the relay
      typeSelect.value = "relay";
      idInput.value = busId;
    }
  }

    renderAssetInspector(node);
  });

  cy.on("tap", "node[?is_equipment]", (evt) => {
    openEquipmentPanel(evt.target.data("parent_bus"));
  });

  // animated power-flow dash offset
  let offset = 0;
  setInterval(() => {
    if (!cy) return;
    offset = (offset + 1) % 20;
    // Only animate edges that are NOT tripped
    cy.edges('[!tripped]').style("line-dash-offset", offset);
  }, 50);
}

// ------------------------------------------------------------
// TELEMETRY WEBSOCKET
// A "generation" counter guards against a subtle but real bug: if the
// Digital Twin backend is restarted while a tab is open, the old socket
// can remain half-open and its onmessage handler can still fire late,
// overwriting the display with stale data from BEFORE the restart, right
// after a newer connection already rendered current data. Each call to
// connectTelemetry() gets its own generation number; a message is only
// applied to the DOM if its socket's generation is still the current one.
// ------------------------------------------------------------
let wsGeneration = 0;

function connectTelemetry() {
  wsGeneration += 1;
  const myGeneration = wsGeneration;
  const ws = new WebSocket(`ws://127.0.0.1:8001/ws/telemetry/${GRID_ID}`);

  ws.onopen = () => console.log(`WebSocket connected to Digital Twin (gen ${myGeneration})`);
  ws.onerror = (err) => console.error("WebSocket error:", err);
  ws.onclose = () => {
    console.log(`WebSocket disconnected (gen ${myGeneration}) -- retrying in 2s`);
    setTimeout(connectTelemetry, 2000);
  };

  ws.onmessage = (event) => {
    if (myGeneration !== wsGeneration) return; // stale socket, ignore
    const state = JSON.parse(event.data);
    latestGridState = state;
    renderTelemetry(state);
  };
}

function renderTelemetry(state) {
  // System status
  setText("statStatus", state.simulation_status || "UNKNOWN");
  document.getElementById("statStatus").className =
    state.simulation_status === "COMPLETED" ? "badge-green" : "badge-red";
  setText("statTimeStep", `t=${state.time_step || 0}`);
  setText("statLastEvent", state.last_event || "None");
  setText("statScenario", state.current_scenario || "Baseline");

  // Electrical metrics
  setText("statDemand", `${(state.current_demand_mw ?? 0).toFixed(2)} MW`);
  setText("statGeneration", `${(state.total_generation_mw ?? 0).toFixed(2)} MW`);
  const maxLoad = state.max_line_loading_percent ?? 0;
  const maxLoadEl = document.getElementById("statMaxLoad");
  maxLoadEl.textContent = `${maxLoad.toFixed(1)}%`;
  maxLoadEl.className = maxLoad > 100 ? "badge-red" : "badge-green";

  // Security metrics
  setText("statOverloadCount", state.overloaded_line_count || 0);
  const linesEl = document.getElementById("statOverloadLines");
  if (state.overloaded_line_count > 0 && state.overloaded_line_ids) {
    linesEl.textContent = `Lines: ${state.overloaded_line_ids.join(", ")}`;
    linesEl.classList.remove("hidden");
  } else {
    linesEl.classList.add("hidden");
  }

  // Grid Resilience Index
  if (state.resilience) {
    const gri = state.resilience.grid_resilience_index;
    const griEl = document.getElementById("griScore");
    griEl.textContent = gri.toFixed(1);
    griEl.className = "gri-score " + (gri >= 80 ? "badge-green" : gri >= 50 ? "badge-amber" : "badge-red");
    setText("griVoltage", state.resilience.voltage_score.toFixed(1));
    setText("griLoading", state.resilience.loading_score.toFixed(1));
    setText("griSecurity", state.resilience.security_score.toFixed(1));
  }

  if (selectedBus) {
    const liveLoad = state.bus_loads?.[selectedBus] ?? 0;
    document.getElementById("currentLoad").textContent = `${Number(liveLoad).toFixed(2)} MW`;

    if (cy) {
      const node = cy.getElementById(selectedBus);
      if (node && node.length) renderAssetInspector(node, true); 
    }
  }

  // Currently-overloaded edges on the graph
  if (cy) {
    cy.edges().removeClass("overloaded");
    if (state.overloaded_line_count > 0 && state.overloaded_line_ids) {
      state.overloaded_line_ids.forEach(id => {
        const el = cy.getElementById(`line${id}`);
        if (el) el.addClass("overloaded");
      });
    }
  }

  // Highest-demand facilities -- glow any bus within 90% of the current
  // peak load, so a genuine cluster of hotspots lights up together, not
  // just a single arbitrary "#1" bus.
  if (cy && state.bus_loads) {
    cy.nodes().removeClass("high-demand");
    const loads = Object.values(state.bus_loads).filter(v => v > 0);
    if (loads.length > 0) {
      const peak = Math.max(...loads);
      const threshold = peak * 0.9;
      Object.entries(state.bus_loads).forEach(([busId, load]) => {
        if (load >= threshold && load > 0) {
          const el = cy.getElementById(busId);
          if (el) el.addClass("high-demand");
        }
      });
    }
  }

  // NOTE: the old "Asset Health (SURVEA Test Feed)" card that used to render
  // here was removed -- Project SURVEA now has its own dedicated Streamlit
  // dashboard that shows this same asset_registry data through its actual
  // trained Random Forest/LSTM models, which is a strictly better answer
  // than this twin's own crude scenario_engine threshold labels. This
  // twin's UI stays focused on physics: topology, power flow, contingency,
  // and the switchgear/fault-injection controls that actually DRIVE what
  // SURVEA observes. state.health / state.asset_health are still sent over
  // the websocket (SURVEA's digital_twin_client.py depends on them) --
  // only the redundant display card here was removed.

}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

// ------------------------------------------------------------
// FACILITY CONTROL (single-bus load command)
// ------------------------------------------------------------
function applyLoadCommand() {
  const val = document.getElementById("loadInput").value;
  const resultEl = document.getElementById("loadCommandResult");
  const btn = document.getElementById("applyLoadBtn");

  if (!selectedBus) { resultEl.textContent = "Click a facility on the graph first."; resultEl.className = "gri-sub badge-amber"; return; }
  if (!val) { resultEl.textContent = "Enter a value first."; resultEl.className = "gri-sub badge-amber"; return; }

  // Freeze the target bus at click time -- if the user clicks a DIFFERENT
  // node while this request is still in flight, this variable (not the
  // possibly-changed `selectedBus`) is what the response applies to, and
  // the button being disabled below prevents overlapping requests
  // entirely, which is what caused the confusing "wrong bus in the error"
  // report: a slow request for an earlier bus resolving after a newer bus
  // was already selected on screen.
  const targetBus = selectedBus;
  const newMw = val;

  btn.disabled = true;
  btn.textContent = "Applying...";
  resultEl.textContent = "";

  fetch(`${API_URL}/change_load/${targetBus}?new_mw=${newMw}&grid=${GRID_ID}`, { method: "POST" })
    .then(async (res) => {
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Command failed");
      return data;
    })
    .then(data => {
      resultEl.textContent = data.action;
      resultEl.className = "gri-sub badge-green";
      document.getElementById("loadInput").value = "";

      // Optimistic immediate update -- don't wait for the next WebSocket
      // tick (up to 1s away) to reflect what we already know just
      // succeeded. Only applies if the user is still looking at the same
      // facility they just changed.
      if (selectedBus === targetBus) {
        document.getElementById("currentLoad").textContent = `${Number(newMw).toFixed(2)} MW`;
      }
    })
    .catch(err => {
      resultEl.textContent = `Bus ${targetBus}: ${err.message}`;
      resultEl.className = "gri-sub badge-red";
    })
    .finally(() => {
      btn.disabled = false;
      btn.textContent = "Apply Load Command";
    });
}

// ------------------------------------------------------------
// STRESS TEST (idempotent, calls /stress_test/{grid})
// ------------------------------------------------------------
function initStressTestControls() {
  const loadSlider = document.getElementById("loadSlider");
  const derateSlider = document.getElementById("derateSlider");
  const loadValueEl = document.getElementById("loadSliderValue");
  const derateValueEl = document.getElementById("derateSliderValue");

  loadSlider.addEventListener("input", () => {
    loadValueEl.textContent = `${loadSlider.value}%`;
  });
  derateSlider.addEventListener("input", () => {
    derateValueEl.textContent = `${derateSlider.value}%`;
  });

  document.getElementById("applyStressBtn").addEventListener("click", () => {
    const loadMultiplier = Number(loadSlider.value) / 100;
    const derateMultiplier = Number(derateSlider.value) / 100;
    const resultEl = document.getElementById("stressResult");
    const btn = document.getElementById("applyStressBtn");

    btn.disabled = true;
    resultEl.textContent = "Applying stress test...";
    resultEl.className = "gri-sub";

    fetch(`${API_URL}/stress_test/${GRID_ID}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ load_multiplier: loadMultiplier, derate_multiplier: derateMultiplier })
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Stress test failed");
        return data;
      })
      .then(data => {
        resultEl.textContent = `Applied. Max line loading now ${data.max_line_loading_percent}%.`;
        resultEl.className = data.max_line_loading_percent > 100 ? "gri-sub badge-red" : "gri-sub badge-green";
      })
      .catch(err => {
        // If you see "Failed to fetch" here specifically (as opposed to a
        // clean error message), it almost always means the Digital Twin
        // server crashed on an unhandled exception for this request --
        // check that terminal's traceback, not just this message.
        resultEl.textContent = `FAILED: ${err.message}`;
        resultEl.className = "gri-sub badge-red";
      })
      .finally(() => {
        btn.disabled = false;
      });
  });
}

// ------------------------------------------------------------
// N-1 CONTINGENCY STATUS (polled, not streamed)
// Shows WHICH specific lines/generators are insecure, not just a count,
// and highlights those lines on the graph in amber so you can see exactly
// where the grid's hidden risk is sitting, not just that risk exists.
// ------------------------------------------------------------
function pollContingencyStatus() {
  fetch(`${API_URL}/contingency/${GRID_ID}`)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then(data => {
      const summaryEl = document.getElementById("contingencyStatus");
      const detailEl = document.getElementById("contingencyDetail");

      if (!data || data.n_minus_1_secure === undefined) {
        summaryEl.innerHTML = `<span class="gri-sub">Scanning... (first scan can take up to 30s after startup)</span>`;
        detailEl.innerHTML = "";
        // Result not ready yet -- retry in 5s instead of waiting the full
        // 15s poll interval. Stops as soon as the cache has a real result.
        setTimeout(pollContingencyStatus, 5000);
        return;
      }

      if (data.n_minus_1_secure) {
        summaryEl.innerHTML = `<span class="badge-green">&#9679; N-1 SECURE</span>`;
        detailEl.innerHTML = "";
        if (cy) cy.edges().removeClass("contingency-risk");
        return;
      }

      summaryEl.innerHTML = `<span class="pulse-dot"></span><span class="badge-red">${data.insecure_contingency_count} insecure contingenc${data.insecure_contingency_count === 1 ? "y" : "ies"}</span>`;

      // List exactly which lines and generators are insecure
      const insecureLines = Object.entries(data.lines || {}).filter(([, v]) => !v.secure).map(([id]) => id);
      const insecureGens = Object.entries(data.generators || {}).filter(([, v]) => !v.secure).map(([id]) => id);

      let detailHtml = "";
      if (insecureLines.length) {
        detailHtml += `<p class="gri-sub" style="margin-top:8px;">Lines at risk if lost: <strong>${insecureLines.join(", ")}</strong></p>`;
      }
      if (insecureGens.length) {
        detailHtml += `<p class="gri-sub">Generators at risk if lost: <strong>${insecureGens.join(", ")}</strong></p>`;
      }
      detailEl.innerHTML = detailHtml;

      // Highlight those specific lines on the graph
      if (cy) {
        cy.edges().removeClass("contingency-risk");
        insecureLines.forEach(id => {
          const el = cy.getElementById(`line${id}`);
          if (el) el.addClass("contingency-risk");
        });
      }
    })
    .catch(() => {
      // Fetch failed (network error, non-JSON response, etc.) --
      // retry in 5s so a transient hiccup doesn't leave the panel
      // stuck on "Scanning..." forever with no recovery path.
      setTimeout(pollContingencyStatus, 5000);
    });
}

// ------------------------------------------------------------
// TESTING CONSOLE (SURVEA scenario generation)
// Calls the new /degrade_asset, /tick_assets, /weather_event endpoints so a
// tester can push specific assets toward failure, age everything forward
// uniformly, or run a combined weather stressor -- all reflected on the
// next telemetry tick via state.health / state.asset_health.
// ------------------------------------------------------------
function initTestingConsole() {
  const resultEl = document.getElementById("testConsoleResult");
  if (!resultEl) return; // page doesn't have the testing console card

  function showResult(text, cls) {
    resultEl.textContent = text;
    resultEl.className = `gri-sub ${cls}`;
  }

  const degradeBtn = document.getElementById("degradeAssetBtn");
  if (degradeBtn) degradeBtn.addEventListener("click", () => {
    const asset_type = document.getElementById("degradeAssetType").value;
    const asset_id = Number(document.getElementById("degradeAssetId").value);
    const severity = Number(document.getElementById("degradeSeverity").value) || 1.0;

    if (Number.isNaN(asset_id)) { showResult("Enter an asset ID first.", "badge-amber"); return; }

    fetch(`${API_URL}/degrade_asset/${GRID_ID}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ asset_type, asset_id, severity })
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Degrade failed");
        return data;
      })
      .then(data => showResult(data.action, "badge-green"))
      .catch(err => showResult(`FAILED: ${err.message}`, "badge-red"));
  });

  const tickBtn = document.getElementById("tickAssetsBtn");
  if (tickBtn) tickBtn.addEventListener("click", () => {
    fetch(`${API_URL}/tick_assets/${GRID_ID}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ severity: 1.0 })
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Tick failed");
        return data;
      })
      .then(() => showResult("All assets aged forward by one time step.", "badge-green"))
      .catch(err => showResult(`FAILED: ${err.message}`, "badge-red"));
  });

  const weatherBtn = document.getElementById("weatherHeatwaveBtn");
  if (weatherBtn) weatherBtn.addEventListener("click", () => {
    fetch(`${API_URL}/weather_event/${GRID_ID}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event_type: "HEATWAVE", severity: 1.0 })
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Weather event failed");
        return data;
      })
      .then(data => showResult(data.action, "badge-green"))
      .catch(err => showResult(`FAILED: ${err.message}`, "badge-red"));
  });
}

window.forceAssetTrip = function(assetType, assetId) {
  let endpoint = assetType === "generator" ? "trip_generator" : "trip_transformer";
  
  fetch(`${API_URL}/${endpoint}/${GRID_ID}/${assetId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ trip_type: "FORCED_OUTAGE" })
  })
    .then(res => res.json())
    .then(data => {
      // The websocket will pick up the state change on the next tick
      console.log(`Forced outage on ${assetType} ${assetId}`);
    })
    .catch(err => console.error("Failed to force outage:", err));
};

// ------------------------------------------------------------
// ASSET INSPECTOR
// Repurposed from a raw sensor-field dump (that's now SURVEA's job, with
// real trained-model verdicts instead of this twin's crude threshold
// labels) into what the physics testbed actually needs: a quick identity/
// status line, plus switchgear controls for every breaker connected to the
// selected asset -- "trip/close the breakers around this asset" without
// hunting for the right line on the graph.
// ------------------------------------------------------------
// Guards against the render-storm flicker: the telemetry websocket can
// tick many times a second, but the breaker list only needs to be
// re-fetched a couple times a second at most, and should only touch the
// DOM when the fetched data actually differs from what's shown.
// ------------------------------------------------------------
// ASSET INSPECTOR
// ------------------------------------------------------------
let lastBreakerFetchTime = 0;
let lastBreakerFetchBus = null;
let lastBreakerDataSignature = null;
let breakerRequestToken = 0;
const BREAKER_REFRESH_THROTTLE_MS = 1000;

function renderAssetInspector(node, isRefresh = false) {
  const card = document.getElementById("assetInspectorCard");
  if (!card) return;

  const nodeType = node.data("node_type");
  const busId = node.id();

  if (nodeType === "JUNCTION") {
    card.classList.add("hidden");
    return;
  }

  card.classList.remove("hidden");

  let identityLine = `Bus ${busId} (${nodeType})`;
  if (nodeType === "GENERATOR") {
    const g = latestGridState?.asset_health?.generators?.[node.data("gen_id")];
    if (g) identityLine += ` &mdash; <span style="color:${g.fault_class === 'Normal' ? '#4ade80' : '#f87171'};">${g.fault_class}</span>`;
  } else if (nodeType === "TRANSFORMER") {
    const t = latestGridState?.asset_health?.transformers?.[node.data("trafo_id")];
    if (t) identityLine += ` &mdash; <span style="color:${t.fault_class === 'Normal' ? '#4ade80' : '#f87171'};">${t.fault_class}</span>`;
  }

  document.getElementById("assetInspectorTitle").textContent = `Asset Inspector`;

  // Generate the manual trip button logic based on asset type
  let manualTripHtml = "";
  if (nodeType === "GENERATOR") {
    manualTripHtml = `
      <hr style="border-color: #333; margin: 12px 0;">
      <button class="action-btn" style="width:100%; background:#dc2626; border-color:#991b1b;" 
              onclick="forceAssetTrip('generator', ${busId})">
        FORCE GENERATOR OUTAGE
      </button>`;
  } else if (nodeType === "TRANSFORMER") {
    manualTripHtml = `
      <hr style="border-color: #333; margin: 12px 0;">
      <button class="action-btn" style="width:100%; background:#dc2626; border-color:#991b1b;" 
              onclick="forceAssetTrip('transformer', ${busId})">
        FORCE TRANSFORMER OUTAGE
      </button>`;
  }

  // Inject skeleton
  if (!isRefresh) {
    document.getElementById("assetInspectorBody").innerHTML = `
      <p id="inspectorIdentity" style="margin-bottom:12px;">${identityLine}</p>
      <p style="color:var(--text-dim); font-size:12px; margin-bottom:6px;">LINES CONNECTED TO THIS ASSET</p>
      <div id="adjacentBreakersList"><span class="gri-sub">Loading...</span></div>
      <hr style="border-color: #333; margin: 12px 0;">
      <p style="color:var(--text-dim); font-size:11px;"><em>Tip: Click any dashed line on the graph to trip/restore it directly.</em></p>
      ${manualTripHtml}
    `;
    lastBreakerDataSignature = null;
    lastBreakerFetchBus = null;
  } else {
    const idEl = document.getElementById("inspectorIdentity");
    if (idEl) idEl.innerHTML = identityLine;
  }

  const now = Date.now();
  if (isRefresh && lastBreakerFetchBus === busId && (now - lastBreakerFetchTime) < BREAKER_REFRESH_THROTTLE_MS) {
    return;
  }
  lastBreakerFetchTime = now;
  lastBreakerFetchBus = busId;

  const myRequestToken = ++breakerRequestToken;

  fetch(`${API_URL}/adjacent_breakers/${GRID_ID}/${busId}`)
    .then(res => res.json())
    .then(data => {
      if (myRequestToken !== breakerRequestToken) return; 

      const listEl = document.getElementById("adjacentBreakersList");
      if (!listEl) return;

      if (!data.breakers || data.breakers.length === 0) {
        if (lastBreakerDataSignature !== "empty") {
          listEl.innerHTML = `<span class="gri-sub">No lines connected to this bus.</span>`;
          lastBreakerDataSignature = "empty";
        }
        return;
      }

      const signature = JSON.stringify(data.breakers.map(b => [b.line_id, b.breaker_state]));
      if (signature === lastBreakerDataSignature) return;
      lastBreakerDataSignature = signature;

      // REMOVED THE TRIP BUTTONS - NOW ONLY SHOWS STATUS
      listEl.innerHTML = data.breakers.map(b => {
        const isOpen = b.breaker_state === "OPEN";
        return `
          <div style="padding:4px 0; border-bottom:1px solid var(--border-subtle);">
            <span style="font-size: 13px;">Line ${b.line_id} (Bus ${b.from_bus}&harr;${b.to_bus})</span>
            <span class="${isOpen ? 'badge-red' : 'badge-green'}" style="font-size:10px; float:right; margin-top:2px;">
                ${b.breaker_state}
            </span>
          </div>`;
      }).join("");
    })
    .catch(err => console.error("Failed to load adjacent breakers:", err));
}

function toggleBreaker(lineId, isCurrentlyOpen) {
  const endpoint = isCurrentlyOpen ? "close_breaker" : "trip_breaker";
  fetch(`${API_URL}/${endpoint}/${GRID_ID}/${lineId}`, { method: "POST" })
    .then(res => res.json())
    .then(() => {
      if (selectedBus && cy) {
        const node = cy.getElementById(selectedBus);
        if (node && node.length) {
          // User just took an action -- bypass the throttle so the result
          // shows immediately instead of waiting for the next window.
          lastBreakerFetchTime = 0;
          renderAssetInspector(node, true);
        }
      }
      const edge = cy?.getElementById(`line${lineId}`);
      if (edge && edge.length) {
        edge.data("tripped", !isCurrentlyOpen);
        edge.toggleClass("line-tripped", !isCurrentlyOpen);
      }
    })
    .catch(err => console.error(`Failed to ${endpoint}:`, err));
}

// ------------------------------------------------------------
// SUBSTATION EQUIPMENT PANEL (Context-Aware Controls)
// ------------------------------------------------------------
function openEquipmentPanel(busId) {
  fetch(`${API_URL}/substation_equipment/${GRID_ID}/${busId}`)
    .then(res => res.json())
    .then(data => {
      let overlay = document.getElementById("equipmentModalOverlay");
      if (!overlay) {
        overlay = document.createElement("div");
        overlay.id = "equipmentModalOverlay";
        overlay.className = "equipment-modal-overlay";
        overlay.innerHTML = `<div class="equipment-modal" style="width: 450px;">
          <button id="equipmentModalClose" class="equipment-modal-close">&times;</button>
          <h2 id="equipmentModalTitle"></h2>
          <div id="equipmentModalBody"></div>
        </div>`;
        document.body.appendChild(overlay);
        overlay.addEventListener("click", (e) => {
          if (e.target === overlay || e.target.id === "equipmentModalClose") {
            overlay.classList.add("hidden");
          }
        });
      }

      document.getElementById("equipmentModalTitle").textContent = `Bus ${data.bus_id} Equipment Bay (${data.node_type})`;
      
      document.getElementById("equipmentModalBody").innerHTML = data.equipment.map(eq => {
        let badgeClass = "badge-green";
        let actionVerb = "Toggle";

        // 1. Determine Badge Color
        if (eq.status === "OPEN" || eq.status === "OUT OF SERVICE" || eq.status.includes("MAINTENANCE")) {
          badgeClass = "badge-amber";
        }
        if (eq.name === "Earth Switch" && eq.status === "CLOSED") {
          badgeClass = "badge-red"; // Danger: Live parts are earthed
        }

        // 2. Determine Power System Action Verb
        if (eq.status === "CLOSED") {
            actionVerb = "OPEN";
        } else if (eq.status === "OPEN") {
            actionVerb = "CLOSE";
        } else if (eq.status === "IN SERVICE") {
            actionVerb = "TAKE OUT";
        } else {
            // Catches OUT OF SERVICE or MAINTENANCE FLAGGED
            actionVerb = "RESTORE";
        }

        return `
        <div class="equipment-row" style="display:flex; justify-content:space-between; align-items:center; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="flex-grow:1; font-size:14px; color:#e2e8f0;">${eq.name}</span>
          <span class="${badgeClass}" style="font-size:11px; margin-right:15px; min-width:110px; text-align:center;">${eq.status}</span>
          <button class="action-btn" style="width:auto; padding:6px 12px; font-size:11px; background:#3b82f6; border-color:#2563eb;" 
                  onclick="toggleEquipment(${busId}, '${eq.name}')">
            ${actionVerb}
          </button>
        </div>
        `;
      }).join("");

      overlay.classList.remove("hidden");
    })
    .catch(err => console.error("Failed to load substation equipment:", err));
}

// Attach the global function so the inline onclick HTML can find it
window.toggleEquipment = function(busId, equipmentName) {
  fetch(`${API_URL}/toggle_equipment/${GRID_ID}/${busId}/${encodeURIComponent(equipmentName)}`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      // Re-fetch and re-render the modal instantly to show the new state
      openEquipmentPanel(busId);
    })
    .catch(err => console.error("Failed to toggle equipment:", err));
};


// ------------------------------------------------------------
// PANEL TOGGLE
// ------------------------------------------------------------
function initPanelToggle() {
  const panel = document.getElementById("sidePanel");
  const btn = document.getElementById("togglePanelBtn");
  btn.addEventListener("click", () => {
    const isHidden = panel.classList.toggle("hidden");
    btn.textContent = isHidden ? "Show Command Center" : "Hide Command Center";
  });
}

// ------------------------------------------------------------
// BOOTSTRAP
// ------------------------------------------------------------
window.addEventListener("DOMContentLoaded", () => {
  loadTopology();
  connectTelemetry();
  initPanelToggle();
  initStressTestControls();
  initTestingConsole();
  document.getElementById("applyLoadBtn").addEventListener("click", applyLoadCommand);

  pollContingencyStatus();
  setInterval(pollContingencyStatus, 8000);
});