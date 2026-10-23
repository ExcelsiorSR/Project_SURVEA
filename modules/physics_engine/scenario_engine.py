import pandapower as pp
import random

def _clamp(value, low, high):
    """Keeps a simulated feature inside the realistic range observed in the
    corresponding SURVEA dataset, so degraded assets stay in-distribution
    for its models instead of drifting into physically implausible values."""
    return max(low, min(high, value))

def apply_load_multiplier(net, multiplier: float):
    """Scales the active and reactive power of all loads in the network."""
    net.load['p_mw'] = net.load['p_mw'] * multiplier
    net.load['q_mvar'] = net.load['q_mvar'] * multiplier
    return net

def derate_lines(net, derate_multiplier: float):
    """Reduces the maximum thermal current capacity of all transmission lines."""
    net.line['max_i_ka'] = net.line['max_i_ka'] * derate_multiplier
    return net

def simulate_transformer_aging(asset_registry, trafo_id: int, severity: float = 1.0, load_factor: float = 1.0):
    """
    Simulates the chemical breakdown of transformer cellulose and oil.
    Includes healthy baseline initialization and continuous ambient sensor noise.
    """
    if trafo_id in asset_registry["transformers"]:
        trafo = asset_registry["transformers"][trafo_id]

        # Initialize with healthy (negative deviation) baselines instead of flat 0.0
        if "fault_mode" not in trafo:
            trafo["H2"] = random.uniform(-0.9, -0.6)
            trafo["CH4"] = random.uniform(-0.9, -0.6)
            trafo["C2H2"] = random.uniform(-0.9, -0.6)
            trafo["C2H4"] = random.uniform(-0.9, -0.6)
            trafo["C2H6"] = random.uniform(-0.9, -0.6)
            trafo["CO"] = random.uniform(-0.9, -0.6)
            trafo["fault_mode"] = random.choice(["ARCING", "THERMAL"])
            trafo["fault_class"] = "Normal"
            trafo["fault_code"] = 0

        # Exponential stress multiplier
        stress_multiplier = severity * (1.0 + max(0, load_factor - 0.8)**2 * 5.0)
        mode = trafo["fault_mode"]

        # Ambient sensor noise so charts stay "alive"
        def ambient(): return random.uniform(-0.02, 0.02)

        if mode == "ARCING":
            trafo["C2H2"] = _clamp(trafo["C2H2"] + random.uniform(0.15, 0.45) * stress_multiplier + ambient(), -1.3, 2.8)
            trafo["H2"] = _clamp(trafo["H2"] + random.uniform(0.05, 0.20) * stress_multiplier + ambient(), -1.3, 2.8)
            trafo["CH4"] = _clamp(trafo["CH4"] + random.uniform(0.0, 0.05) * stress_multiplier + ambient(), -1.3, 2.8)
            trafo["C2H4"] = _clamp(trafo["C2H4"] + random.uniform(0.0, 0.05) * stress_multiplier + ambient(), -1.3, 2.8)
            trafo["C2H6"] = _clamp(trafo["C2H6"] + ambient(), -1.3, 2.8)
            trafo["CO"] = _clamp(trafo["CO"] + ambient(), -1.3, 2.8)
        else:  # THERMAL
            trafo["CH4"] = _clamp(trafo["CH4"] + random.uniform(0.15, 0.40) * stress_multiplier + ambient(), -1.3, 2.8)
            trafo["C2H4"] = _clamp(trafo["C2H4"] + random.uniform(0.15, 0.40) * stress_multiplier + ambient(), -1.3, 2.8)
            trafo["C2H6"] = _clamp(trafo["C2H6"] + random.uniform(0.05, 0.15) * stress_multiplier + ambient(), -1.3, 2.8)
            trafo["CO"] = _clamp(trafo["CO"] + random.uniform(0.05, 0.20) * stress_multiplier + ambient(), -1.3, 2.8)
            trafo["C2H2"] = _clamp(trafo["C2H2"] + ambient(), -1.3, 2.8)
            trafo["H2"] = _clamp(trafo["H2"] + ambient(), -1.3, 2.8)

        trafo["rul_days"] = max(0.0, trafo["rul_days"] - (random.uniform(1.0, 3.0) * stress_multiplier))
        trafo["dga_score"] = round(max(trafo[g] for g in ("H2", "CH4", "C2H2", "C2H4", "C2H6", "CO")), 3)

        # Fault classification logic
        if mode == "ARCING":
            if trafo["C2H2"] > 2.0:
                trafo["fault_class"], trafo["fault_code"] = "D2 - High Energy Discharge", 3
            elif trafo["C2H2"] > 1.0:
                trafo["fault_class"], trafo["fault_code"] = "D1 - Low Energy Discharge", 2
            elif trafo["C2H2"] > 0.4:
                trafo["fault_class"], trafo["fault_code"] = "Partial Discharge", 1
            else:
                trafo["fault_class"], trafo["fault_code"] = "Normal", 0
        else:
            hottest = max(trafo["CH4"], trafo["C2H4"])
            if hottest > 2.0:
                trafo["fault_class"], trafo["fault_code"] = "T3 - Thermal Fault (>700C)", 6
            elif hottest > 1.3:
                trafo["fault_class"], trafo["fault_code"] = "T2 - Thermal Fault (300-700C)", 5
            elif hottest > 0.6:
                trafo["fault_class"], trafo["fault_code"] = "T1 - Thermal Fault (<300C)", 4
            else:
                trafo["fault_class"], trafo["fault_code"] = "Normal", 0

    return asset_registry

def simulate_generator_wear(asset_registry, gen_id: int, wear_rate: float = 1.0, load_factor: float = 1.0):
    """
    Simulates mechanical bearing wear AND thermal stress.
    Cascading Stress: Loads > 90% drastically accelerate Temp_Rise_Rate and Bearing_Amplitude.
    """
    if gen_id in asset_registry["generators"]:
        gen = asset_registry["generators"][gen_id]

        gen.setdefault("Bearing_Frequency_Hz", 50.0) # Adjusted for 50Hz standard
        gen.setdefault("Bearing_Amplitude_mm_s", 0.0)
        gen.setdefault("Temperature_C", 40.0)
        gen.setdefault("Temp_Rise_Rate_C_min", 0.0)

        # Thermal stress scales quadratically with extreme overloads
        stress_multiplier = wear_rate * (1.0 + max(0, load_factor - 0.9)**2 * 15.0)

        gen["Bearing_Amplitude_mm_s"] = _clamp(
            gen["Bearing_Amplitude_mm_s"] + random.uniform(0.05, 0.30) * stress_multiplier, 0.0, 11.77
        )
        gen["Bearing_Frequency_Hz"] = _clamp(
            gen["Bearing_Frequency_Hz"] + random.uniform(-0.2, 0.2) * wear_rate, 47.0, 52.0
        )
        gen["Temperature_C"] = _clamp(
            gen["Temperature_C"] + random.uniform(0.2, 1.2) * stress_multiplier, 22.82, 113.21
        )
        gen["Temp_Rise_Rate_C_min"] = _clamp(
            gen["Temp_Rise_Rate_C_min"] + random.uniform(0.02, 0.12) * stress_multiplier, 0.0, 6.0
        )
        gen["Thermal_Runaway_Indicator"] = 1 if gen["Temp_Rise_Rate_C_min"] > 2.0 else 0

        gen["rul_days"] = max(0.0, gen["rul_days"] - (random.uniform(0.8, 2.5) * stress_multiplier))
        gen["vibration_amp"] = gen["Bearing_Amplitude_mm_s"]

        amp = gen["Bearing_Amplitude_mm_s"]
        if amp < 2.3:
            gen["ISO10816_Zone"] = "A"
        elif amp < 4.5:
            gen["ISO10816_Zone"] = "B"
        elif amp < 7.1:
            gen["ISO10816_Zone"] = "C"
        else:
            gen["ISO10816_Zone"] = "D"

        if gen["Thermal_Runaway_Indicator"] == 1:
            gen["fault_class"], gen["fault_code"] = "Thermal Runaway", 4
        elif gen["Temp_Rise_Rate_C_min"] > 1.0:
            gen["fault_class"], gen["fault_code"] = "Thermal Warning", 3
        elif gen["ISO10816_Zone"] == "D":
            gen["fault_class"], gen["fault_code"] = "Severe Fault", 2
        elif gen["ISO10816_Zone"] == "C":
            gen["fault_class"], gen["fault_code"] = "Moderate Fault", 1
        else:
            gen["fault_class"], gen["fault_code"] = "Normal", 0

    return asset_registry

def simulate_breaker_degradation(asset_registry, breaker_id: int, friction_factor: float = 1.0, load_factor: float = 1.0):
    """
    Simulates trip-coil friction, contact wear, and SF6 gas leakage.
    Cascading Stress: I^2R heating scales contact temperature directly with load.
    """
    if breaker_id in asset_registry["circuit_breakers"]:
        cb = asset_registry["circuit_breakers"][breaker_id]

        cb.setdefault("TCCS_Peak_Current_A", 3.0)
        cb.setdefault("TCCS_Duration_ms", 10.0)
        cb.setdefault("Contact_Travel_Time_ms", 32.0)
        cb.setdefault("Contact_Temperature_C", 35.0)
        cb.setdefault("Gas_Pressure_bar", 7.0)

        # Contact temperature scales with square of the load factor (I^2R)
        thermal_multiplier = friction_factor * (load_factor ** 2)

        cb["TCCS_Peak_Current_A"] = _clamp(
            cb["TCCS_Peak_Current_A"] + random.uniform(0.05, 0.30) * friction_factor, 2.78, 7.55
        )
        cb["TCCS_Duration_ms"] = _clamp(
            cb["TCCS_Duration_ms"] + random.uniform(1.0, 4.0) * friction_factor, 9.38, 29.73
        )
        cb["Contact_Travel_Time_ms"] = _clamp(
            cb["Contact_Travel_Time_ms"] + random.uniform(0.5, 2.5) * friction_factor, 31.04, 65.93
        )
        cb["Contact_Temperature_C"] = _clamp(
            cb["Contact_Temperature_C"] + random.uniform(0.3, 1.5) * thermal_multiplier, 34.61, 80.71
        )
        cb["Gas_Pressure_bar"] = _clamp(
            cb["Gas_Pressure_bar"] - random.uniform(0.01, 0.05) * friction_factor, 5.20, 7.13
        )

        cb["rul_days"] = max(0.0, cb["rul_days"] - (random.uniform(0.5, 2.0) * friction_factor))
        cb["tccs_delay_ms"] = cb["TCCS_Duration_ms"]

        travel = cb["Contact_Travel_Time_ms"]
        duration = cb["TCCS_Duration_ms"]
        if travel > 55.0:
            cb["fault_class"], cb["fault_code"] = "Mechanical Jamming - Severe", 5
        elif travel > 45.0:
            cb["fault_class"], cb["fault_code"] = "Mechanical Jamming - Mild", 4
        elif duration > 24.0:
            cb["fault_class"], cb["fault_code"] = "Coil Degradation - Severe", 2
        elif travel > 38.0:
            cb["fault_class"], cb["fault_code"] = "Friction Wear", 3
        elif duration > 16.0:
            cb["fault_class"], cb["fault_code"] = "Coil Degradation - Early", 1
        else:
            cb["fault_class"], cb["fault_code"] = "Normal", 0

    return asset_registry

def simulate_relay_degradation(asset_registry, relay_id: int, noise_factor: float = 1.0, load_factor: float = 1.0):
    """
    Simulates degradation of numerical relay logic (CT saturation / noise).
    Cascading Stress: Extreme overloads push the apparent impedance closer to the trip zone.
    """
    if relay_id in asset_registry["relays"]:
        relay = asset_registry["relays"][relay_id]

        relay.setdefault("V_rms", 0.71)
        relay.setdefault("I_rms", 0.36)
        relay.setdefault("V_peak", 1.06)
        relay.setdefault("I_peak", 0.53)
        relay.setdefault("Impedance_Z", 1.40)

        stress_multiplier = noise_factor * max(1.0, load_factor)

        relay["I_rms"] = _clamp(relay["I_rms"] + random.uniform(0.02, 0.08) * stress_multiplier, 0.21, 1.39)
        relay["I_peak"] = _clamp(relay["I_peak"] + random.uniform(0.05, 0.25) * stress_multiplier, 0.53, 4.11)
        relay["Impedance_Z"] = _clamp(relay["Impedance_Z"] - random.uniform(0.02, 0.10) * stress_multiplier, 0.14, 1.40)
        relay["V_rms"] = _clamp(relay["V_rms"] - random.uniform(0.002, 0.010) * stress_multiplier, 0.57, 0.78)
        relay["V_peak"] = _clamp(relay["V_peak"] + random.uniform(-0.01, 0.01) * stress_multiplier, 0.99, 1.14)

        relay["logic_integrity"] = max(0.0, relay["logic_integrity"] - (random.uniform(0.5, 2.0) * stress_multiplier))

        z = relay["Impedance_Z"]
        if z > 0.9:
            relay["fault_class"], relay["relay_fault_class"] = "Normal", 0
        elif z > 0.40:
            relay["fault_class"], relay["relay_fault_class"] = "Moderate Impedance Fault", 2
        elif z > 0.28:
            relay["fault_class"], relay["relay_fault_class"] = "Elevated Fault Current", 1
        else:
            relay["fault_class"], relay["relay_fault_class"] = "Critical Zone Fault", 3

    return asset_registry

# ==========================================================
#   EXTENDED SCENARIO EVENTS
# ==========================================================

def simulate_generator_trip(net, asset_registry, gen_id: int, trip_type: str = "FORCED_OUTAGE"):
    """Forces a generator out of service and stamps the event onto the asset registry."""
    if gen_id in net.gen.index:
        net.gen.at[gen_id, 'in_service'] = False
    else:
        raise ValueError(f"Generator {gen_id} not found in network.")

    if gen_id in asset_registry["generators"]:
        gen_record = asset_registry["generators"][gen_id]
        gen_record["fault_class"] = trip_type
        gen_record["rul_days"] = 0.0

    return net, asset_registry

def simulate_weather_event(net, asset_registry, event_type: str = "HEATWAVE", severity: float = 1.0):
    """Applies a grid-wide weather stress scenario (HEATWAVE / STORM / COLD_SNAP)."""
    if event_type == "HEATWAVE":
        derate_factor = max(0.5, 1.0 - (0.10 * severity))
        net = derate_lines(net, derate_multiplier=derate_factor)
        for trafo_id in asset_registry["transformers"]:
            asset_registry = simulate_transformer_aging(asset_registry, trafo_id, severity=1.5 * severity, load_factor=1.2)

    elif event_type == "STORM":
        derate_factor = max(0.3, 1.0 - (0.25 * severity))
        net = derate_lines(net, derate_multiplier=derate_factor)
        for cb_id in asset_registry["circuit_breakers"]:
            asset_registry = simulate_breaker_degradation(asset_registry, cb_id, friction_factor=2.0 * severity, load_factor=1.0)

    elif event_type == "COLD_SNAP":
        net = apply_load_multiplier(net, multiplier=1.0 + (0.20 * severity))

    else:
        raise ValueError(f"Unknown weather event_type: '{event_type}'. Use HEATWAVE, STORM, or COLD_SNAP.")

    return net, asset_registry

def ramp_down_renewables(net, ramp_percent: float, renewable_gen_ids: list = None):
    """Curtails renewable generator output by ramp_percent (0-100)."""
    if not (0 <= ramp_percent <= 100):
        raise ValueError("ramp_percent must be between 0 and 100.")

    target_ids = renewable_gen_ids if renewable_gen_ids is not None else list(net.gen.index)

    for gid in target_ids:
        if gid in net.gen.index:
            current_mw = net.gen.at[gid, 'p_mw']
            net.gen.at[gid, 'p_mw'] = current_mw * (1 - ramp_percent / 100.0)

    return net