import math
import numpy as np
import scipy

# from phase_plot import (
#     cosine_fit_data,
#     a_bpm_23_phases,
#     a_bpm_32_phases,
#     b_bpm_23_phases,
#     b_bpm_32_phases,
#     c_bpm_23_phases,
#     c_bpm_32_phases,
#     d_bpm_23_phases,
#     d_bpm_32_phases,
#     rf_phases,
# )
# from pv_definitions import Energy_SCL_LLRF_FCM23a, Energy_SCL_LLRF_FCM23d


import math
import numpy as np
import scipy


def energy_from_bpm_phases(phase_bpm_23: float,
phase_bpm_32: float,
energy_guess_ev: float,
phase_offset_bpm_23: float = 56.0608,
phase_offset_bpm_32: float = -171.2920,
position_bpm_23: float = 93.662,
position_bpm_32: float = 164.681,
bpm_frequency: float = 402.5E6
) -> float:
    delta_z = position_bpm_32 - position_bpm_23
    delta_phase_bpm_23 = phase_bpm_23 - phase_offset_bpm_23
    delta_phase_bpm_32 = phase_bpm_32 - phase_offset_bpm_32
    delta_phase_bpm_23 = np.radians(delta_phase_bpm_23)
    delta_phase_bpm_32 = np.radians(delta_phase_bpm_32)
    omega_bpm = 2 * math.pi * bpm_frequency
    energy_rest = scipy.constants.physical_constants["proton mass energy equivalent in MeV"][0] * 1E6
    c = scipy.constants.speed_of_light
    gamma_zero = (energy_rest + energy_guess_ev) / energy_rest
    beta_zero = math.sqrt(1 - 1 / gamma_zero ** 2)
    delta_phi_energy_guess = omega_bpm * delta_z / c / beta_zero
    n = math.floor(delta_phi_energy_guess / 2 / math.pi)
    beta = omega_bpm * delta_z / c / (2 * n * math.pi + (delta_phase_bpm_32 - delta_phase_bpm_23))
    gamma = math.sqrt(1 / (1 - beta ** 2))
    energy_kin = (gamma - 1) * energy_rest
    return energy_kin


import yaml

Phi_Offset_SCL_Diag_BPM23 = 56.0608
Phi_Offset_SCL_Diag_BPM32 = -171.2920

def make_fitted_plot(cavity):
        with open('energy_scan_cosine_fitted_data_without_cavity_a.yml', 'r') as file:
            cosine_energy_fit = yaml.safe_load(file)
        data =  cosine_energy_fit[cavity]
        if cavity == 'a':
            return
        amplitude = data['cosine_fitted_amplitude']
        avg_value  =data['avg_value']
        offset = data['phase_offset']
        print((986e6-972e6)/amplitude)
        cavity_phase = np.arccos((986e6-972e6)/amplitude) - offset
        print(f'{cavity} {cavity_phase=}')
        y = [amplitude*(np.cos(np.radians(x+offset))) + avg_value for x in energy_vs_phase_dataset[cavity]['RF_PHASES']]
        # plt.plot(energy_vs_phase_dataset[cavity]['RF_PHASES'], y, label='fitted data')
        # plt.legend()

if __name__ == "__main__":

    with open("cavity_phase_scans_without_A_unwrapped_ACC_PHASES.yml", "r") as file:
        phase_scan_data = yaml.safe_load(file)
    energy_vs_phase_dataset = {}
    for cavity, data in phase_scan_data["scans"].items():
        if cavity == 'a':
            continue
        energy_vs_phase_dataset[cavity] = {}
        energy_vs_phase_dataset[cavity]["RF_PHASES"] = data["RF_PHASES"]
        energy_vs_phase_dataset[cavity]["DELTA_ENERGY"] = []
        e_init = 945e6
        bpm_23_phases = data["BPM_PHASES"]["BPM23"]
        bpm_32_phases = data["BPM_PHASES"]["BPM32"]
        energies = {
            "a": e_init,
            "b": e_init, #958.2301700877831e6,
            "c": 958.2301700877831e6, #972.2218858065837e6,
            "d": 972.2218858065837e6,
        }
        for p_23, p_32 in zip(bpm_23_phases, bpm_32_phases):
            current_energy = energy_from_bpm_phases(
                    p_23,
                    p_32,
                    energies[cavity],
                    Phi_Offset_SCL_Diag_BPM23,
                    Phi_Offset_SCL_Diag_BPM32,
                )
            if len(energy_vs_phase_dataset[cavity]['DELTA_ENERGY']) == 0:
                delta_e = 0
            else:
                delta_e = current_energy - energy_vs_phase_dataset[cavity]["DELTA_ENERGY"][-1]
            if abs(delta_e) > 5e6:
                current_energy -= np.sign(delta_e)*2*25.24157*1e6
            energy_vs_phase_dataset[cavity]["DELTA_ENERGY"].append(
                current_energy
            )
    
        from matplotlib import pyplot as plt
        plt.figure()
        plt.title(f'Cavity {str(cavity).upper()}')
        plt.xlabel('RF Phase [deg]')
        plt.ylabel('Delta Energy [eV]')
        plt.plot(
            energy_vs_phase_dataset[cavity]["RF_PHASES"],
            energy_vs_phase_dataset[cavity]["DELTA_ENERGY"],
            label = 'energy scan measurement'
        )
        make_fitted_plot(cavity)

    cavity_d_phases = energy_vs_phase_dataset['d']['RF_PHASES']
    cavity_d_energies = energy_vs_phase_dataset['d']['DELTA_ENERGY']
    diffs = []
    for ind, energy in enumerate(cavity_d_energies):
        if cavity_d_phases[ind] > 50.:
            diffs.append(1e9)
        else:
            diffs.append(np.abs(986e6-energy))
    index_of_min_diff = np.argmin(diffs)
    phase_at_min_diff = cavity_d_phases[index_of_min_diff]
    energy_at_min_diff = cavity_d_energies[index_of_min_diff]
    print('Min diff Phase [deg] ', cavity_d_phases[index_of_min_diff])
    plt.scatter([phase_at_min_diff], [energy_at_min_diff])
    plt.xlabel('RF Phases [deg]')
    plt.ylabel('Delta Energy [eV]')
    plt.show()
    with open("phase_energy_scan_unwrapped_without_cavity_A.yml", "w") as file:
        yaml.dump(energy_vs_phase_dataset, file)
    cavity_A = energy_from_bpm_phases(
        -175.9220137950059,
        -144.69940224251516,
        945e6,
        56.0608,
        -171.2920,
    )
    cavity_B = energy_from_bpm_phases(
        177.66498597908117, 115.80991810168379, 958.2301700877831e6, 56.0608, -171.2920
    )
    cavity_C = energy_from_bpm_phases(
        173.11527241639283, 20.96911926826099, 972.2218858065837e6, 56.0608, -171.2920
    )
    cavity_D = energy_from_bpm_phases(
        173.05124900971686, 20.49368981580418, 972.2218858065837e6, 56.0608, -171.2920
    )

    energies = {
        "Cavity A": cavity_A,
        "Cavity B": cavity_B,
        "Cavity C": cavity_C,
        "Cavity D": cavity_D,
    }

    with open("calculate_energies.yml", "w") as file:
        yaml.dump(energies, file)
