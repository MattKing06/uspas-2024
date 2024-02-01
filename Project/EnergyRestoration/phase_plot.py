import yaml
import yaml
from matplotlib import pyplot as plt
import numpy as np

data = {}
with open("all_cavity_phase_scans.yml", "r") as file:
    data = yaml.safe_load(file)

# print(data)
from matplotlib import pyplot as plt

rf_phases = data["scans"]["a"]["RF_PHASES"]
a_bpm_23_phases = data["scans"]["a"]["BPM_PHASES"]["BPM23"]
a_bpm_32_phases = data["scans"]["a"]["BPM_PHASES"]["BPM32"]

plt.figure()
plt.plot(rf_phases, a_bpm_23_phases, label="bpm_23")
plt.plot(rf_phases, a_bpm_32_phases, label="bpm_32")
plt.title("Phase Scan Cavity a")
plt.legend()


rf_phases = data["scans"]["b"]["RF_PHASES"]
b_bpm_23_phases = data["scans"]["b"]["BPM_PHASES"]["BPM23"]
b_bpm_32_phases = data["scans"]["b"]["BPM_PHASES"]["BPM32"]
plt.figure()
plt.plot(rf_phases, b_bpm_23_phases, label="bpm_23")
plt.plot(rf_phases, b_bpm_32_phases, label="bpm_32")
plt.title("Phase Scan Cavity b")
plt.legend()

rf_phases = data["scans"]["c"]["RF_PHASES"]
c_bpm_23_phases = data["scans"]["c"]["BPM_PHASES"]["BPM23"]
c_bpm_32_phases = data["scans"]["c"]["BPM_PHASES"]["BPM32"]
plt.figure()
plt.plot(rf_phases, c_bpm_23_phases, label="bpm_23")
plt.plot(rf_phases, c_bpm_32_phases, label="bpm_32")
plt.title("Phase Scan Cavity c")
plt.legend()


rf_phases = data["scans"]["d"]["RF_PHASES"]
d_bpm_23_phases = data["scans"]["d"]["BPM_PHASES"]["BPM23"]
d_bpm_32_phases = data["scans"]["d"]["BPM_PHASES"]["BPM32"]
plt.figure()
plt.plot(rf_phases, d_bpm_23_phases, label="bpm_23")
plt.plot(rf_phases, d_bpm_32_phases, label="bpm_32")
plt.title("Phase Scan Cavity d")
plt.legend()
# plt.show()

from uspas_pylib.harmonic_data_fitting_lib import fitCosineFunc, CosFittingScorer

cosine_fit_data = {}
for cavity, dataset in data["scans"].items():
    rf_phases = dataset["RF_PHASES"]
    bpm_32_phases = dataset["BPM_PHASES"]["BPM32"]
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

with open("cosine_fitted_data.yml", "w") as file:
    yaml.safe_dump(cosine_fit_data)
