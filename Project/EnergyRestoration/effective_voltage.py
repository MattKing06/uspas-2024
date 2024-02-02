from phase_scan import bpm_frequency
from pv_definitions import (
    Pos_SCL_Diag_BPM32,
    Pos_SCL_Diag_BPM23,
    Pos_SCL_LLRF_FCM23a,
    Pos_SCL_LLRF_FCM23b,
    Pos_SCL_LLRF_FCM23c,
    Pos_SCL_LLRF_FCM23d,
    Energy_SCL_LLRF_FCM23a,
)
import math
import scipy
import yaml

p_mass_ev = 938.272e6
e = 1.602176634e-19
with open("all_cavity_scan_cosine_fitted_data.yml", "r") as file:
    cosine_data = yaml.safe_load(file)
with open("calculate_energies.yml", "r") as file:
    accelerated_energies = yaml.safe_load(file)
with open("all_cavity_phase_scans_unwrapped.yml", "r") as file:
    phase_scan_data = yaml.safe_load(file)

cosine_indices = [
    "a",
    "b",
    "c",
    "d",
]
acclerated_indices = [
    "Cavity A",
    "Cavity B",
    "Cavity C",
    "Cavity D",
]
distances = [
    Pos_SCL_LLRF_FCM23a,
    Pos_SCL_LLRF_FCM23b,
    Pos_SCL_LLRF_FCM23c,
    Pos_SCL_LLRF_FCM23d,
]
for i in range(0, len(cosine_data)):
    cosine_amplitude = cosine_data[cosine_indices[i]]["cosine_fitted_amplitude"]
    phase_offset = cosine_data[cosine_indices[i]]["phase_offset"]
    rf_phase = phase_scan_data[f"initial_for_cavity_{cosine_indices[i]}"][
        "init_cav_phase"
    ]

    if i == 0:
        energy_before_cavity = Energy_SCL_LLRF_FCM23a
    else:
        energy_before_cavity = accelerated_energies[acclerated_indices[i - 1]]
    energy_after_cavity = accelerated_energies[acclerated_indices[i]]

    delta_z = Pos_SCL_Diag_BPM32 - Pos_SCL_Diag_BPM23

    # gamma
    gamma = energy_after_cavity / p_mass_ev + 1
    # beta
    beta = math.sqrt(1 - (1 / gamma))
    if cosine_indices[i] == "d":
        v_eff_in_voltage = (cosine_amplitude * math.pow(gamma * beta, 3)) / (
            delta_z * 0.98e9
        )
        v_eff_in_ev = v_eff_in_voltage / e
        print(f"V Eff for {acclerated_indices[i]} [MeV]: ", v_eff_in_ev / 1e6)
        # (energy_before_cavity - energy_after_cavity)/math.cos(rf_phase + phase_offset)
    else:
        v_eff_in_voltage = (cosine_amplitude * math.pow(gamma * beta, 3)) / (
            delta_z * energy_after_cavity
        )
        v_eff_in_ev = v_eff_in_voltage / e
        print(f"V Eff for {acclerated_indices[i]} [MeV]: ", v_eff_in_ev / 1e6)
