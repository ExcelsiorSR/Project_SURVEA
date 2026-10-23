clear; clc;

% 1. System Parameters
f = 50;
fs = 10000;
t = 0:1/fs:0.1;
omega = 2*pi*f;

num_samples = 500;   % Number of unique fault scenarios to generate

% Best Practice: Preallocate the matrix for speed
dataset = zeros(num_samples, 6); 

for k = 1:num_samples
    
    % 2. Randomize Pre-Fault Conditions
    Vm = 0.9 + 0.2*rand();   
    Im = 0.3 + 0.4*rand();    
    phi = pi/12 + (pi/6)*rand();  
    
    Va = Vm * sin(omega*t);
    Ia = Im * sin(omega*t - phi);
    
    % 3. Randomize Fault Parameters
    fault_type = randi([0 3]);  
    % 0 = Normal, 1 = SLG, 2 = LL, 3 = 3-phase
    
    fault_start = 0.03 + 0.02*rand(); 
    fault_end   = fault_start + 0.02;
    fault_zone  = (t >= fault_start) & (t <= fault_end);
    
    Va_faulty = Va;
    Ia_faulty = Ia;
    
    % 4. Apply Fault Physics
    if fault_type == 1  
        Va_faulty(fault_zone) = 0.2 * Vm * sin(omega*t(fault_zone)); 
        Ia_faulty(fault_zone) = 4 * Im * sin(omega*t(fault_zone));
        
    elseif fault_type == 2  
        Va_faulty(fault_zone) = 0.5 * Vm * sin(omega*t(fault_zone)); 
        Ia_faulty(fault_zone) = 3 * Im * sin(omega*t(fault_zone));
        
    elseif fault_type == 3  
        Va_faulty(fault_zone) = 0.1 * Vm * sin(omega*t(fault_zone)); 
        Ia_faulty(fault_zone) = 6 * Im * sin(omega*t(fault_zone));
    end
    
    % 5. Inject Custom Gaussian Noise
    SNR_dB = 25 + 10*rand(); 
    SNR = 10^(SNR_dB/10);
    
    Pv = mean(Va_faulty.^2);
    Pi = mean(Ia_faulty.^2);
    
    noise_V = sqrt(Pv/SNR) * randn(size(Va));
    noise_I = sqrt(Pi/SNR) * randn(size(Ia));
    
    Va_noisy = Va_faulty + noise_V;
    Ia_noisy = Ia_faulty + noise_I;
    
    % 6. Feature Extraction for AI
    V_rms = rms(Va_noisy);
    I_rms = rms(Ia_noisy);
    V_peak = max(abs(Va_noisy));
    I_peak = max(abs(Ia_noisy));
    
    Z = V_rms / (I_rms + 1e-6); % 1e-6 prevents division by zero
    
    % Store the calculated features in our preallocated matrix
    dataset(k, :) = [V_rms, I_rms, V_peak, I_peak, Z, fault_type];
end

% 7. Export Data with Column Headers
% Convert the matrix into a table so we can add headers
varNames = {'V_rms', 'I_rms', 'V_peak', 'I_peak', 'Impedance_Z', 'Fault_Class'};
T = array2table(dataset, 'VariableNames', varNames);

% Write to CSV
writetable(T, 'relay_dataset.csv');

disp('Project SURVEA: Relay Dataset Generated Successfully!');