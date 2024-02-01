import yaml
import math
from uspas_pylib.harmonic_data_fitting_lib import fitCosineFunc, CosFittingScorer
from mebt_rf_scan_to_cav_params_VA_hint_0 import (
    L_dist,
    bpm_frequency,
    e_kin_ini,
    mass,
    gamma,
    beta,
    v_light,
)

phase_scan_data = {}
with open("phase_scan_data.yml", "r") as file:
    phase_scan_data = yaml.safe_load(file)

min_bpm_phase = min(phase_scan_data["BPM_PHASES"])
print(f'{min_bpm_phase=}')
max_acc_index = phase_scan_data["BPM_PHASES"].index(min_bpm_phase)
max_acc = phase_scan_data["RF_PHASES"][max_acc_index]
print(f'Max accelerating RF phase = ', max_acc)
min_acc = max_acc - 90
print(f'Min accelerating RF phase = ', min_acc)
(
    results,
    _,
) = fitCosineFunc(phase_scan_data["RF_PHASES"], phase_scan_data["BPM_PHASES"])
amp, phase_offset, avg_val = results
print(f'fitted amplitude = ', amp)
print(f'fitted phase_offset = ', phase_offset)
t = (min_bpm_phase - phase_offset) / bpm_frequency
print(f'{t = } ')
delta_beta = (L_dist/(t*v_light)) - beta
print(f'{delta_beta = } ')

delta_energy = mass*math.pow(gamma,3)*math.pow(beta,3)*(v_light*L_dist)*((2*math.pi)/bpm_frequency)
print(f'{delta_energy=}')
delta_energy = e_kin_ini*L_dist*t
print(f'{delta_energy=}')
veff = delta_energy/1.6e-19
print(f'{veff=}')