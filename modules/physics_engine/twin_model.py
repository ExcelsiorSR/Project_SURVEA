# =============================================
#              MODULE IMPORTS
# =============================================

import pandapower as pp
import pandapower.networks as nw
import copy
import random
from modules.physics_engine.grid_metrics import (
    get_topology_metrics, 
    get_security_metrics, 
    get_electrical_metrics, 
    get_health_metrics, 
    get_observation_vector,
    get_resilience_index)

from modules.physics_engine.scenario_engine import (
    apply_load_multiplier, 
    derate_lines,
    simulate_transformer_aging,
    simulate_generator_wear,
    simulate_breaker_degradation,
    simulate_relay_degradation,
    simulate_generator_trip,
    simulate_weather_event,
    ramp_down_renewables)


# ==========================================================
#              DIGITAL TWIN MODEL ARCHITECTURE
# ==========================================================

class TwinModel():
    

    def __init__(self, grid_type='39'):
        '''Initializes the IEEE 39-Bus System as the foundational Digital Twin and stores it inside the object as self.net.'''
        
        self.current_time_step = 0
        self.state_history = {}

        self.grid_type = grid_type
        print(f'Initializing IEEE {grid_type}-Bus System')
        self.current_state = None
        self.previous_state = None
        self.simulation_status = "NOT_STARTED"
        self.current_scenario = "Baseline"
        self.event_history = []
        
        if grid_type == '39':
            self.net = nw.case39() #Loads the 39 bus system.
        elif grid_type == '118':
            self.net = nw.case118() #Loads the 118 bus system.
        else:
            raise ValueError("Unsupported Grid Type. Choose '39' or '118'. ")

        # Snapshot the ORIGINAL nameplate load/line ratings before any scenario is ever applied. 
        # This is the fixed anchor point the stress-test slider scales from - so "150%" always means "150% of what this IEEE case ships with," 
        # regardless of what scenarios were applied before or how many times the slider has been moved.
        self.baseline_load_p_mw = self.net.load['p_mw'].copy()
        self.baseline_load_q_mvar = self.net.load['q_mvar'].copy()
        self.baseline_max_i_ka = self.net.line['max_i_ka'].copy()
        
        self.asset_registry = {
            "transformers": {
                idx: {
                    "fault_class": "Normal", "fault_code": 0, "rul_days": 100.0,
                    "dga_score": 0.0,
                    "H2": 0.0, "CH4": 0.0, "C2H2": 0.0, "C2H4": 0.0, "C2H6": 0.0, "CO": 0.0,
                    # persistent per-asset degradation trajectory, assigned once
                    "fault_mode": random.choice(["ARCING", "THERMAL"]),
                }
                for idx in self.net.trafo.index
            },
            "generators": {
                idx: {
                    "fault_class": "Normal", "fault_code": 0, "rul_days": 100.0,
                    "vibration_amp": 0.0,
                    "Bearing_Frequency_Hz": 50.0, "Bearing_Amplitude_mm_s": 0.0,
                    "Temperature_C": 40.0, "Temp_Rise_Rate_C_min": 0.0,
                    "Thermal_Runaway_Indicator": 0, "ISO10816_Zone": "A",
                }
                for idx in self.net.gen.index
            },
            "circuit_breakers": {
                idx: {
                    "fault_class": "Normal", "fault_code": 0, "rul_days": 100.0,
                    "tccs_delay_ms": 10.0,
                    "TCCS_Peak_Current_A": 3.0, "TCCS_Duration_ms": 10.0,
                    "Contact_Travel_Time_ms": 32.0, "Contact_Temperature_C": 35.0,
                    "Gas_Pressure_bar": 7.0,
                    "breaker_state": "CLOSED", "operation_count": 0, # switchgear state - separate from the degradation
                }
                for idx in self.net.line.index
            },
            "relays": {
                idx: {
                    "fault_class": "Normal", "relay_fault_class": 0, "logic_integrity": 100.0,
                    "V_rms": 0.71, "I_rms": 0.36, "V_peak": 1.06, "I_peak": 0.53, "Impedance_Z": 1.40,
                }
                for idx in self.net.bus.index
            }
        }

    
    def get_current_state(self):
        simulation_summary = {}

        topology_metics = get_topology_metrics(self.net)
        electrical_metrics = get_electrical_metrics(self.net)
        security_metrics = get_security_metrics(self.net)
        health_metrics = get_health_metrics(self.net)

        simulation_summary["asset_health"] = self.asset_registry
        simulation_summary["health"] = health_metrics
        
        if self.event_history:
            last_event = self.event_history[-1]
        else:
            last_event = "None"

        simulation_summary["last_event"] = last_event
        simulation_summary["simulation_status"] = self.simulation_status
        simulation_summary["current_scenario"] = self.current_scenario
        simulation_summary["ai_observation"] = get_observation_vector(self.net)

        simulation_summary.update(topology_metics)
        simulation_summary.update(electrical_metrics)
        simulation_summary.update(security_metrics)
        simulation_summary["resilience"] = get_resilience_index(self.net)
        
        return simulation_summary
    
    def update_state(self, simulation_summary, simulation_status, event):

        self.previous_state = self.current_state
        self.current_state = simulation_summary
        self.simulation_status = simulation_status
        self.event_history.append(event)

        #Overwrite the lagging event with the actual current event
        self.current_state["last_event"] = event

        # --- THE TEMPORAL ENGINE ---
        # 1. Tick the clock forward
        self.current_time_step += 1
        
        # 2. Add the timestamp to the summary
        self.current_state["time_step"] = self.current_time_step
        
        # 3. Save a deep copy to the historical ledger
        self.state_history[self.current_time_step] = copy.deepcopy(self.current_state)

    def age_all_assets(self, severity=1.0):
        """Ages all critical assets in the registry by one time step."""
        
        for trafo_id in self.asset_registry["transformers"].keys():
            self.asset_registry = simulate_transformer_aging(self.asset_registry, trafo_id, severity)
            
        for gen_id in self.asset_registry["generators"].keys():
            self.asset_registry = simulate_generator_wear(self.asset_registry, gen_id, severity)
            
        for cb_id in self.asset_registry["circuit_breakers"].keys():
            self.asset_registry = simulate_breaker_degradation(self.asset_registry, cb_id, severity)
            
        for relay_id in self.asset_registry["relays"].keys():
            self.asset_registry = simulate_relay_degradation(self.asset_registry, relay_id, severity)
            
        print(f"[CLOCK] Assets aged by {severity}x severity factor.")

    def tick_assets(self, severity=1.0):
        '''
        Advances asset degradation by one time step AND records the resulting
        state to state_history -- age_all_assets() alone mutates the
        registry but never surfaces the result. This is what lets a test
        harness (or Project SURVEA's own validation scripts) step through a
        realistic multi-step degradation trajectory (rising DGA/vibration/
        TCCS-delay, falling RUL, eventual fault_class transitions) rather
        than only ever seeing a single static snapshot.
        '''
        self.age_all_assets(severity)
        summary = self.get_current_state()
        self.update_state(summary, "COMPLETED", f"Assets ticked forward ({severity}x severity)")
        return summary

    def degrade_asset(self, asset_type: str, asset_id: int, severity: float = 1.0):
        '''
        Pushes ONE specific asset toward failure, for generating targeted, reproducible test fixtures for Random Forest / LSTM models 
        - e.g. "push transformer 3 toward HIGH_ENERGY_ARCING" - instead of only being able to age every asset uniformly via age_all_assets()/tick_assets().

        asset_type: "transformer" | "generator" | "circuit_breaker" | "relay"
        asset_id: index into the corresponding asset_registry sub-dict
        '''
        asset_type = asset_type.lower().strip()

        if asset_type in ("transformer", "transformers"):
            if asset_id not in self.asset_registry["transformers"]:
                raise ValueError(f"Transformer {asset_id} not found in asset registry.")
            self.asset_registry = simulate_transformer_aging(self.asset_registry, asset_id, severity)
        elif asset_type in ("generator", "generators"):
            if asset_id not in self.asset_registry["generators"]:
                raise ValueError(f"Generator {asset_id} not found in asset registry.")
            self.asset_registry = simulate_generator_wear(self.asset_registry, asset_id, severity)
        elif asset_type in ("circuit_breaker", "circuit_breakers", "breaker"):
            if asset_id not in self.asset_registry["circuit_breakers"]:
                raise ValueError(f"Circuit breaker {asset_id} not found in asset registry.")
            self.asset_registry = simulate_breaker_degradation(self.asset_registry, asset_id, severity)
        elif asset_type in ("relay", "relays"):
            if asset_id not in self.asset_registry["relays"]:
                raise ValueError(f"Relay {asset_id} not found in asset registry.")
            self.asset_registry = simulate_relay_degradation(self.asset_registry, asset_id, severity)
        else:
            raise ValueError(
                f"Unknown asset_type '{asset_type}'. Use transformer, generator, circuit_breaker, or relay."
            )

        event = f"Manually degraded {asset_type} {asset_id} ({severity}x severity)"
        self.event_history.append(event)
        summary = self.get_current_state()
        self.update_state(summary, "COMPLETED", event)
        return summary

    def run_baseline_simulation(self):
        '''Runs deterministic AC Power Flow to establish baseline grid health'''

        print('Running Newton - Raphson Power Flow')

        try:

            self.simulation_status = "RUNNING"
            self.event_history.append("Baseline Simulation Started")
            # pp.runpp exectues the AC Power Flow equations 
            pp.runpp(self.net, solver ='nr')

            simulation_summary = self.get_current_state()

            print('\n--- Simulation Successful ---')
            print(f'Total Buses: {len(self.net.bus)}')
            print(f'Total Lines: {len(self.net.line)}')
            print(f'Total Load: {len(self.net.load)}')

            #Displays a Snippet of Bus Voltages to prove the Physics Engine is working
            print('\n Sample Bus Voltages (per unit):')
            print(self.net.res_bus.vm_pu.head())

            #Displays a Snippet of Line Thermal Loading
            print('\n Sample Line Loading (%):')
            print(self.net.res_line.loading_percent.head())

            self.update_state(simulation_summary, "COMPLETED", "Baseline Simulation Completed")
            return simulation_summary

        except pp.LoadflowNotConverged:
            self.simulation_status = "FAILED"
            self.event_history.append("Simulation Failed")
            print('CRITICAL‼: Powerflow did not converge, Grid has Collapsed!')

        
            

    def inject_line_fault(self, line_index):
        '''Simulates a Physical line outage by taking a transmission line out of service'''

        print(f'\n[!] INJECTING FAULT: TRIPPING LINE {line_index}')
        self.event_history.append(f"Line {line_index} Tripped ")

        #Checks if the line is available and currently in service
        if line_index  in self.net.line.index:
            self.net.line.at[line_index, 'in_service'] = False

            # Every line has exactly one associated breaker (asset_registry is keyed 1:1 by line index) - a line trip IS a breaker opening, 
            # so the switchgear state updates in lockstep with the physics, not as a separate/optional step.
            if line_index in self.asset_registry["circuit_breakers"]:
                cb = self.asset_registry["circuit_breakers"][line_index]
                cb["breaker_state"] = "OPEN"
                cb["operation_count"] = cb.get("operation_count", 0) + 1



            try:
                #Re-runs the Power Flow with the updated Topology
                pp.runpp(self.net, solver='nr')
                summary = self.get_current_state()

                self.update_state(summary,"COMPLETED",f"Line {line_index} Tripped")
                print('--- Post Fault Simulation Successful ---')

                #Checks for Thermal overloads(>100%)
                overloaded_lines = self.net.res_line[self.net.res_line.loading_percent > 100]


                if not overloaded_lines.empty:
                    print('\nCRITICAL WARNING: The Following Lines are thermally overloaded:')
                    print(overloaded_lines[['loading_percent']])
                else:
                    print('\n Grid Stabilized. No Thermal Overloads detected after Fault')

            except pp.LoadflowNotConverged:
                print('FATAL: Power Flow did not Converge ! The Fault caused a Cascading Blackout.')

        else:
            print('Error: Invalid Line Index')  

        def close_breaker(self, line_index):
            '''
            Restores a tripped line by closing its breaker - the counterpart to inject_line_fault. 
            Lives on TwinModel so both directions of a switchgear operation go through the same consistent path.
            '''
        print(f'\n[!] CLOSING BREAKER: RESTORING LINE {line_index}')

        if line_index not in self.net.line.index:
            raise ValueError(f"Line {line_index} not found in network.")

        self.net.line.at[line_index, 'in_service'] = True

        if line_index in self.asset_registry["circuit_breakers"]:
            cb = self.asset_registry["circuit_breakers"][line_index]
            cb["breaker_state"] = "CLOSED"
            cb["operation_count"] = cb.get("operation_count", 0) + 1

        try:
            pp.runpp(self.net, solver='nr')
            summary = self.get_current_state()
            self.update_state(summary, "COMPLETED", f"Line {line_index} Restored")
            self.event_history.append(f"Line {line_index} Restored")
            print('--- Post-Restore Simulation Successful ---')
        except pp.LoadflowNotConverged:
            self.simulation_status = "FAILED"
            self.event_history.append(f"Line {line_index} Restore Failed (non-convergent)")
            print('FATAL: Power Flow did not converge after restoring this line.')

    def get_adjacent_breakers(self, bus_id: int) -> list:
        '''Returns every line/breaker directly connected to a bus -- what
        the frontend's "breakers around this asset" control needs when a
        generator/transformer/load node is selected, since a bus alone
        doesn't tell you which lines touch it.'''
        connected = self.net.line[(self.net.line.from_bus == bus_id) | (self.net.line.to_bus == bus_id)]
        result = []
        for line_id in connected.index:
            cb = self.asset_registry["circuit_breakers"].get(line_id, {})
            result.append({
                "line_id": int(line_id),
                "from_bus": int(connected.at[line_id, "from_bus"]),
                "to_bus": int(connected.at[line_id, "to_bus"]),
                "breaker_state": cb.get("breaker_state", "UNKNOWN"),
                "fault_class": cb.get("fault_class", "Normal"),
            })
        return result



    def change_load(self, bus_id, new_load_mw):
        # 1. Search the dataframe for the load attached to this specific bus
        matching_loads = self.net.load[self.net.load.bus == int(bus_id)].index
        
        if not matching_loads.empty:
            load_index = matching_loads[0] # Grab the specific load index
            self.net.load.at[load_index, "p_mw"] = new_load_mw
            
            # 2. Recalculate power flow
            pp.runpp(self.net, solver='nr')
            summary = self.get_current_state()
            self.update_state(summary, "COMPLETED", f"Load on Bus {bus_id} Updated")
            print("Load Updated Successfully")
        else:
            # 3. Reject the command if it's just a transmission junction
            raise ValueError(f"Physics Error: Bus {bus_id} does not have a load facility attached to it.")

    def trip_generator(self, gen_id, trip_type="FORCED_OUTAGE"):
        '''
        Forces a generator out of service (unplanned trip) and tags the asset registry so downstream health-monitoring models 
        see a clean run-to-failure label on this asset.
        '''

        print(f'\n[!] TRIPPING GENERATOR {gen_id} ({trip_type})')

        self.net, self.asset_registry = simulate_generator_trip(
            self.net, self.asset_registry, gen_id, trip_type
        )
        self.event_history.append(f"Generator {gen_id} Tripped ({trip_type})")

        try:
            pp.runpp(self.net, solver='nr')
            summary = self.get_current_state()
            self.update_state(summary, "COMPLETED", f"Generator {gen_id} Tripped ({trip_type})")
            print('--- Post-Trip Simulation Successful ---')

        except pp.LoadflowNotConverged:
            self.simulation_status = "FAILED"
            self.event_history.append("Simulation Failed")
            print('CRITICAL‼: Powerflow did not converge after generator trip! Cascading blackout risk.')

    def apply_weather_event(self, event_type="HEATWAVE", severity=1.0):
        '''
        Applies a weather-driven stress scenario: HEATWAVE (line derating + transformer aging), STORM (heavier line derating + breaker wear),
        or COLD_SNAP (system-wide load spike).
        '''

        print(f"\n[WEATHER] Applying {event_type} event at severity {severity}x")

        self.net, self.asset_registry = simulate_weather_event(
            self.net, self.asset_registry, event_type, severity
        )
        self.current_scenario = f"Weather Event: {event_type} ({severity}x)"
        self.event_history.append(self.current_scenario)

        try:
            pp.runpp(self.net, solver='nr')
            summary = self.get_current_state()
            self.update_state(summary, "COMPLETED", self.current_scenario)
            print('--- Post-Weather-Event Simulation Successful ---')

        except pp.LoadflowNotConverged:
            self.simulation_status = "FAILED"
            self.event_history.append("Simulation Failed")
            print('CRITICAL‼: Powerflow did not converge after weather event!')

    def ramp_renewables(self, ramp_percent, renewable_gen_ids=None):
        '''Gradually curtails renewable generator output (cloud cover, wind lull, or a forced curtailment order).'''

        print(f"\n[RAMP] Reducing renewable output by {ramp_percent}%")

        self.net = ramp_down_renewables(self.net, ramp_percent, renewable_gen_ids)
        event = f"Renewables ramped down by {ramp_percent}%"
        self.event_history.append(event)

        try:
            pp.runpp(self.net, solver='nr')
            summary = self.get_current_state()
            self.update_state(summary, "COMPLETED", event)
            print('--- Post-Ramp Simulation Successful ---')

        except pp.LoadflowNotConverged:
            self.simulation_status = "FAILED"
            self.event_history.append("Simulation Failed")
            print('CRITICAL‼: Powerflow did not converge after renewable ramp-down!')

    def apply_stress_test(self, load_multiplier: float, derate_multiplier: float):
        '''
        Sets load and line thermal capacity to an ABSOLUTE percentage of the network's ORIGINAL baseline (captured at __init__), 
        not a multiple of whatever the current state happens to be. 
        This is what makes it safe for a UI slider: moving it to 150% always means "150% of nameplate load," whether the slider was at 100% or 250% a moment ago. 
        Contrast with apply_scenario() below, which is cumulative and was only ever meant to be called once at startup.

        load_multiplier: e.g. 1.0 = nameplate load, 2.5 = 250% of nameplate
        derate_multiplier: e.g. 1.0 = full nominal thermal rating, 0.5 = lines derated to half their nominal ampacity
        '''
        print(f"\n[STRESS TEST] Setting load to {load_multiplier*100:.0f}% and line capacity to {derate_multiplier*100:.0f}% of baseline")

        self.net.load['p_mw'] = self.baseline_load_p_mw.values * load_multiplier
        self.net.load['q_mvar'] = self.baseline_load_q_mvar.values * load_multiplier
        self.net.line['max_i_ka'] = self.baseline_max_i_ka.values * derate_multiplier

        self.current_scenario = f"Stress Test (Load {load_multiplier*100:.0f}%, Line Capacity {derate_multiplier*100:.0f}%)"
        self.event_history.append(self.current_scenario)

        try:
            pp.runpp(self.net, solver='nr')
            summary = self.get_current_state()
            self.update_state(summary, "COMPLETED", self.current_scenario)
            print('--- Stress Test Simulation Successful ---')
        except pp.LoadflowNotConverged:
            self.simulation_status = "FAILED"
            self.event_history.append("Simulation Failed")
            print('CRITICAL‼: Powerflow did not converge under this stress level!')

    def apply_scenario(self, load_multiplier: float, derate_multiplier: float):
        '''Stresses the grid to simulate extreme operational limits.'''
        print(f"\n[SCENARIO] Scaling load by {load_multiplier}x and derating lines to {derate_multiplier}x capacity")
        
        # 1. Scale the load
        self.net = apply_load_multiplier(self.net, load_multiplier)
        
        # 2. Derate the lines
        self.net = derate_lines(self.net, derate_multiplier)
        
        # 3. Update state tracking variables
        self.current_scenario = f"Stressed (Load {load_multiplier}x, Cap {derate_multiplier}x)"
        self.event_history.append(self.current_scenario)


# ==================================================
#              TESTING & EXECUTION
# ==================================================

if __name__ == "__main__":
    model = TwinModel(grid_type='118')
    model.apply_scenario(load_multiplier=1.5, derate_multiplier=0.02)
    
    # t=1: Baseline
    model.run_baseline_simulation()
    
    # t=2: Fault Injection
    # Let's trip a less critical line so the grid doesn't instantly collapse
    model.inject_line_fault(10) 
    
    # t=3: Load Adjustment
    model.change_load(bus_id=5, new_load_mw=150)
    
    # Validate the History
    print("\n--- TEMPORAL HISTORY LEDGER ---")
    print(f"Total Time Steps Recorded: {len(model.state_history)}")
    for t, state in model.state_history.items():
        print(f"t={t} | Event: {state['last_event']}")