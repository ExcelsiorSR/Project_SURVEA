% generate_transformer_dga.m
%
% Physics-informed synthetic Dissolved Gas Analysis (DGA) generator for
% power transformers. Fills the one real gap the real dataset (dga_ml_ready.csv)
% has: it only ships STANDARDIZED gas readings, so the true Duval-triangle
% percentages and CO2/O2/H2O can't be reconstructed from it. This script
% generates RAW ppm values instead, from which real Duval percentages and
% ratios fall out naturally -- no placeholder values needed.
%
% Written in plain Octave/MATLAB-core syntax only: no toolboxes (no Control
% System Toolbox, no Simulink, no Statistics Toolbox functions), so this runs
% unmodified on any online Octave compiler (e.g. octave-online.net).
%
% USAGE (from the Octave/MATLAB command line or `octave generate_transformer_dga.m`):
%   generate_transformer_dga()
% Produces: synthetic_transformer_dga.csv in the current directory.
%
% PHYSICS MODEL
% --------------
% Each simulated transformer is assigned one degradation path:
%   0 = HEALTHY      -- stays within IEEE C57.104 normal limits the whole time
%   1 = THERMAL       -- CH4/C2H4/CO rise (cellulose + oil overheating)
%   2 = ARCING        -- C2H2 rises sharply (high-energy discharge -- the
%                        single most dangerous DGA signature)
%   3 = PARTIAL_DISCHARGE -- H2 rises first, with a slower secondary C2H2 rise
%
% Gas growth follows a simple accelerating-aging curve once past each
% transformer's random "onset" time:
%   gas(t) = baseline + growth_rate * max(0, t - onset)^1.4 + noise
% The ^1.4 exponent gives a mildly convex (accelerating) curve -- consistent
% with the Arrhenius-law intuition (IEEE C57.104 / IEC 60599) that insulation
% and oil degradation accelerates once a fault initiates, without requiring
% an actual Arrhenius equation and its activation-energy parameters, which
% we have no measured values for and would otherwise have to invent.

function generate_transformer_dga()
  rand("seed", 42);
  randn("seed", 42);

  n_transformers = 20;
  months_per_unit = 60;  % 5 years of monthly DGA sampling per unit

  % IEEE C57.104 normal/critical thresholds (ppm) -- also shown on the XAI page
  normal_limits   = struct("H2", 150, "CH4", 75,  "C2H2", 3,  "C2H4", 50,  "C2H6", 65,  "CO", 350);
  critical_limits = struct("H2", 400, "CH4", 200, "C2H2", 35, "C2H4", 100, "C2H6", 100, "CO", 700);

  fault_path_names = {"HEALTHY", "THERMAL", "ARCING", "PARTIAL_DISCHARGE"};

  % Pre-open the output file and write the header once
  fid = fopen("synthetic_transformer_dga.csv", "w");
  fprintf(fid, "Timestamp,Transformer_ID,H2,CH4,C2H2,C2H4,C2H6,CO,CO2,O2,H2O,");
  fprintf(fid, "R1_CH4_H2,R2_C2H2_C2H4,R3_C2H2_CH4,R4_C2H4_C2H6,R5_C2H6_CH4,");
  fprintf(fid, "Duval_CH4_pct,Duval_C2H4_pct,Duval_C2H2_pct,IEC_Fault_Label,Fault_Code\n");

  for unit = 1:n_transformers
    transformer_id = sprintf("SYN-T%02d", unit);

    % Roughly a third of units stay healthy for the full observation window
    % -- otherwise every unit in the training set eventually fails, which
    % would bias a classifier toward always predicting a fault.
    if rand() < 0.30
      path = 0;
    else
      path = 1 + floor(rand() * 3);  % 1, 2, or 3
    end

    onset_month = 6 + rand() * (months_per_unit - 12);  % onset sometime after month 6
    severity = 0.6 + rand() * 0.8;  % per-unit severity multiplier, 0.6x-1.4x

    % Baseline (healthy) gas levels -- comfortably inside IEEE normal limits
    base = struct("H2", 20 + rand()*15, "CH4", 15 + rand()*10, "C2H2", 0.2 + rand()*0.5, ...
                  "C2H4", 8 + rand()*10, "C2H6", 10 + rand()*10, "CO", 80 + rand()*40);

    start_year = 2018 + floor(rand() * 5);
    start_month = 1 + floor(rand() * 12);

    for m = 0:(months_per_unit - 1)
      t_past_onset = max(0, m - onset_month);
      accel = t_past_onset ^ 1.4;

      h2   = base.H2   + noise_term();
      ch4  = base.CH4  + noise_term();
      c2h2 = base.C2H2 + noise_term() * 0.3;
      c2h4 = base.C2H4 + noise_term();
      c2h6 = base.C2H6 + noise_term();
      co   = base.CO   + noise_term() * 3;

      if path == 1  % THERMAL
        ch4  = ch4  + severity * 3.5 * accel;
        c2h4 = c2h4 + severity * 5.0 * accel;
        co   = co   + severity * 8.0 * accel;
      elseif path == 2  % ARCING
        c2h2 = c2h2 + severity * 1.2 * accel;
        h2   = h2   + severity * 2.0 * accel;
      elseif path == 3  % PARTIAL_DISCHARGE
        h2   = h2   + severity * 4.0 * accel;
        c2h2 = c2h2 + severity * 0.15 * accel;
      end

      % floor every gas at a small positive value -- concentrations can't be negative
      h2   = max(0.1, h2);
      ch4  = max(0.1, ch4);
      c2h2 = max(0.0, c2h2);
      c2h4 = max(0.1, c2h4);
      c2h6 = max(0.1, c2h6);
      co   = max(0.1, co);

      % CO2/O2/H2O -- simple, independently plausible trends, not tied to the
      % Duval calculation (which only needs CH4/C2H4/C2H2), just filling out
      % the full schema with reasonable, non-fabricated-looking values:
      co2 = 3000 + 6 * m + noise_term() * 50;          % slowly rises with cellulose aging
      o2  = max(500, 20000 - 40 * m + noise_term()*200); % slowly depletes
      h2o = 10 + 0.15 * m + noise_term() * 2;            % slowly rises (moisture ingress)

      eps = 1e-6;
      r1 = ch4 / (h2 + eps);
      r2 = c2h2 / (c2h4 + eps);
      r3 = c2h2 / (ch4 + eps);
      r4 = c2h4 / (c2h6 + eps);
      r5 = c2h6 / (ch4 + eps);

      duval_total = ch4 + c2h4 + c2h2;
      duval_ch4  = 100 * ch4  / (duval_total + eps);
      duval_c2h4 = 100 * c2h4 / (duval_total + eps);
      duval_c2h2 = 100 * c2h2 / (duval_total + eps);

      [label, code] = classify_fault(h2, ch4, c2h2, c2h4, c2h6, co, ...
                                      normal_limits, critical_limits, path);

      year_offset  = floor((start_month - 1 + m) / 12);
      month_of_row = mod(start_month - 1 + m, 12) + 1;
      timestamp = sprintf("01/%02d/%04d 09:00", month_of_row, start_year + year_offset);

      fprintf(fid, "%s,%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,", ...
              timestamp, transformer_id, h2, ch4, c2h2, c2h4, c2h6, co, co2, o2, h2o);
      fprintf(fid, "%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%s,%d\n", ...
              r1, r2, r3, r4, r5, duval_ch4, duval_c2h4, duval_c2h2, label, code);
    end
  end

  fclose(fid);
  printf("Wrote synthetic_transformer_dga.csv (%d transformers x %d months)\n", ...
         n_transformers, months_per_unit);
end


function n = noise_term()
  % Small zero-mean Gaussian noise, reused for every gas reading.
  n = randn() * 2.5;
end


function [label, code] = classify_fault(h2, ch4, c2h2, c2h4, c2h6, co, ...
                                          normal_limits, critical_limits, path)
  % IEEE C57.104-style thresholding, biased toward the gas(es) relevant to
  % this unit's assigned fault path -- mirrors the same encoding used
  % throughout the rest of the project (Fault_Code 0-7) so this file can be
  % concatenated directly with dga_ml_ready.csv for training.
  if h2 > critical_limits.H2 || c2h2 > critical_limits.C2H2
    if path == 2
      label = "D2 - High Energy Discharge"; code = 3;
    elseif path == 3
      label = "D1 - Low Energy Discharge"; code = 2;
    else
      label = "T3 - Thermal Fault (>700C)"; code = 6;
    end
  elseif ch4 > critical_limits.CH4 || c2h4 > critical_limits.C2H4 || co > critical_limits.CO
    label = "T2 - Thermal Fault (300-700C)"; code = 5;
  elseif h2 > normal_limits.H2 || c2h2 > normal_limits.C2H2
    if path == 2 || path == 3
      label = "Partial Discharge"; code = 1;
    else
      label = "T1 - Thermal Fault (<300C)"; code = 4;
    end
  elseif ch4 > normal_limits.CH4 || c2h4 > normal_limits.C2H4 || co > normal_limits.CO
    label = "T1 - Thermal Fault (<300C)"; code = 4;
  else
    label = "Normal"; code = 0;
  end
end
