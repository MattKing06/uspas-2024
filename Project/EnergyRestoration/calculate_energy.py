import math
import numpy as np
import scipy

from phase_plot import (
    cosine_fit_data,
    a_bpm_23_phases,
    a_bpm_32_phases,
    b_bpm_23_phases,
    b_bpm_32_phases,
    c_bpm_23_phases,
    c_bpm_32_phases,
    d_bpm_23_phases,
    d_bpm_32_phases,
    rf_phases,
)
from pv_definitions import Energy_SCL_LLRF_FCM23a, Energy_SCL_LLRF_FCM23d


def energy_from_bpm_phases(
    phase_bpm_23: float,
    phase_bpm_32: float,
    energy_guess_ev: float,
    phase_offset_bpm_23: float = 56.0608,
    phase_offset_bpm_32: float = -171.2920,
    position_bpm_23: float = 93.662,
    position_bpm_32: float = 164.681,
    bpm_frequency: float = 805e6,
) -> float:
    delta_z = position_bpm_32 - position_bpm_23
    delta_phi = np.radians(phase_bpm_32 - phase_bpm_23)
    delta_phi_zero = np.radians(phase_offset_bpm_32 - phase_offset_bpm_23)
    omega_bpm = 2 * math.pi * bpm_frequency

    energy_rest = (
        scipy.constants.physical_constants["proton mass energy equivalent in MeV"][0]
        * 1e6
    )
    c = scipy.constants.speed_of_light
    gamma_zero = (energy_rest + energy_guess_ev) / energy_rest
    beta_zero = math.sqrt(1 - 1 / gamma_zero**2)

    delta_phi_energy_guess = omega_bpm * delta_z / c / beta_zero  # +
    beta = (
        omega_bpm * delta_z / c / (delta_phi_energy_guess + delta_phi - delta_phi_zero)
    )
    # beta = beta_zero + delta_beta
    gamma = math.sqrt(1 / (1 - beta**2))
    energy_kin = (gamma - 1) * energy_rest
    return energy_kin


# phase_offset_32 = cosine_fit_data['a']
cavity_a_init_phase = 142
cavity_b_init_phase = -126
cavity_c_init_phase = -60
cavity_d_init_phase = -28
a_nominal_phase_index = rf_phases.index(cavity_a_init_phase)

b_nominal_phase_index = rf_phases.index(cavity_b_init_phase)


a_energy_calculate = energy_from_bpm_phases(
    a_bpm_23_phases[a_nominal_phase_index],
    a_bpm_32_phases[a_nominal_phase_index],
    Energy_SCL_LLRF_FCM23a,
)
print('Energy Cavity A [MeV]: ', a_energy_calculate / (1e6))


b_nominal_phase_index = rf_phases.index(cavity_b_init_phase)
b_energy_calculate = energy_from_bpm_phases(
    b_bpm_23_phases[b_nominal_phase_index],
    b_bpm_32_phases[b_nominal_phase_index],
    a_energy_calculate,
    phase_offset_bpm_23=a_bpm_23_phases[a_nominal_phase_index],
    phase_offset_bpm_32=a_bpm_32_phases[a_nominal_phase_index]
)
print('Energy Cavity B [MeV]: ', b_energy_calculate / (1e6))


c_nominal_phase_index = rf_phases.index(cavity_c_init_phase)
c_energy_calculate = energy_from_bpm_phases(
    c_bpm_23_phases[c_nominal_phase_index],
    c_bpm_32_phases[c_nominal_phase_index],
    b_energy_calculate,
    phase_offset_bpm_23=b_bpm_23_phases[b_nominal_phase_index],
    phase_offset_bpm_32=b_bpm_32_phases[b_nominal_phase_index]
)
print('Energy Cavity C [MeV]: ', c_energy_calculate / (1e6))


d_nominal_phase_index = rf_phases.index(cavity_d_init_phase)
d_energy_calculate = energy_from_bpm_phases(
    d_bpm_23_phases[d_nominal_phase_index],
    d_bpm_32_phases[d_nominal_phase_index],
    c_energy_calculate,
    phase_offset_bpm_23=c_bpm_23_phases[c_nominal_phase_index],
    phase_offset_bpm_32=c_bpm_32_phases[c_nominal_phase_index]
)
print('Energy Cavity D [MeV]: ', d_energy_calculate / (1e6))


print(f'Cav A: bpm 23/32 at rf phase {rf_phases[a_nominal_phase_index]}  = {a_bpm_23_phases[a_nominal_phase_index]} / {a_bpm_32_phases[a_nominal_phase_index]}')
print(f'Cav B: bpm 23/32 at rf phase {rf_phases[b_nominal_phase_index]}  = {b_bpm_23_phases[b_nominal_phase_index]} / {b_bpm_32_phases[b_nominal_phase_index]}')
print(f'Cav C: bpm 23/32 at rf phase {rf_phases[c_nominal_phase_index]}  = {c_bpm_23_phases[c_nominal_phase_index]} / {c_bpm_32_phases[c_nominal_phase_index]}')
print(f'Cav D: bpm 23/32 at rf phase {rf_phases[d_nominal_phase_index]}  = {d_bpm_23_phases[d_nominal_phase_index]} / {d_bpm_32_phases[d_nominal_phase_index]}')
