import yaml
import yaml
from matplotlib import pyplot as plt
import numpy as np

data = {}
with open("cavity_phase_scans_without_A_unwrapped.yml", "r") as file:
    data = yaml.safe_load(file)

# print(data)
from matplotlib import pyplot as plt

x_label = "RF Cavity Phase [deg]"
y_label = "BPM23 Phase Readback [deg]"
title = "Phase Scan for Cavity "

if "RF_PHASES" in data["scans"]["a"]:
    rf_phases = data["scans"]["a"]["RF_PHASES"]
    a_bpm_23_phases = data["scans"]["a"]["BPM_PHASES"]["BPM23"]
    a_bpm_32_phases = data["scans"]["a"]["BPM_PHASES"]["BPM32"]
    a_init_rf_phase = data["initial_for_cavity_a"]["init_cav_phase"]
    a_init_bpm_32_phase = data["initial_for_cavity_a"]["init_bpm_32_phase"]
    plt.figure()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title + "A")
    # plt.scatter([a_init_rf_phase], [a_init_bpm_32_phase ])
    plt.plot(rf_phases, a_bpm_23_phases, label="bpm_23")
    plt.plot(rf_phases, a_bpm_32_phases, label="bpm_32")
    plt.legend()


rf_phases = data["scans"]["b"]["RF_PHASES"]
b_bpm_23_phases = data["scans"]["b"]["BPM_PHASES"]["BPM23"]
b_bpm_32_phases = data["scans"]["b"]["BPM_PHASES"]["BPM32"]
b_init_rf_phase = data["initial_for_cavity_b"]["init_cav_phase"]
b_init_bpm_32_phase = data["initial_for_cavity_b"]["init_bpm_32_phase"]
plt.figure()
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(title + "B")
# plt.scatter([b_init_rf_phase], [b_init_bpm_32_phase])
plt.plot(rf_phases, b_bpm_23_phases, label="bpm_23")
plt.plot(rf_phases, b_bpm_32_phases, label="bpm_32")
plt.legend()

rf_phases = data["scans"]["c"]["RF_PHASES"]
c_bpm_23_phases = data["scans"]["c"]["BPM_PHASES"]["BPM23"]
c_bpm_32_phases = data["scans"]["c"]["BPM_PHASES"]["BPM32"]
c_init_rf_phase = data["initial_for_cavity_c"]["init_cav_phase"]
c_init_bpm_32_phase = data["initial_for_cavity_c"]["init_bpm_32_phase"]
plt.figure()
# plt.scatter([c_init_rf_phase], [c_init_bpm_32_phase ])
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(title + "C")
plt.plot(rf_phases, c_bpm_23_phases, label="bpm_23")
plt.plot(rf_phases, c_bpm_32_phases, label="bpm_32")
plt.legend()


rf_phases = data["scans"]["d"]["RF_PHASES"]
d_bpm_23_phases = data["scans"]["d"]["BPM_PHASES"]["BPM23"]
d_bpm_32_phases = data["scans"]["d"]["BPM_PHASES"]["BPM32"]
d_init_rf_phase = data["initial_for_cavity_d"]["init_cav_phase"]
d_init_bpm_32_phase = data["initial_for_cavity_d"]["init_bpm_32_phase"]
plt.figure()
# plt.scatter([d_init_rf_phase], [d_init_bpm_32_phase ])
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(title + "D")
plt.plot(rf_phases, d_bpm_23_phases, label="bpm_23")
plt.plot(rf_phases, d_bpm_32_phases, label="bpm_32")
plt.title("Phase Scan Cavity D")
plt.legend()
#plt.show()

from uspas_pylib.harmonic_data_fitting_lib import fitCosineFunc, CosFittingScorer

with open('phase_energy_scan_unwrapped.yml', 'r') as file:
    data = yaml.safe_load(file)
cosine_fit_data = {}
for cavity, dataset in data.items():
    rf_phases = dataset["RF_PHASES"]
    bpm_32_phases = dataset["DELTA_ENERGY"]
    (
        results,
        _,
    ) = fitCosineFunc(rf_phases, bpm_32_phases)
    amp, phase_offset, avg_val = results
    cosine_fit_data[cavity] = {
        "cosine_fitted_amplitude": amp,
        "phase_offset": phase_offset,
        "avg_value": avg_val,
    }
print(cosine_fit_data)

with open("energy_scan_cosine_fitted_data_without_cavity_a.yml", "w") as file:
    yaml.dump(cosine_fit_data, file)
