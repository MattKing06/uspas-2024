from matplotlib import pyplot as plt
import numpy as np

BPM_FREQUENCY = 402.5e6
PROTON_MASS_KG = 1.67262192e-27
EV_PER_JOULE = 1 / 1.60218e-19

def get_average_relative_difference(values_list: list[float]):
    ''' 
        Utility function that calculates average relative difference
        using the pairwise differences then np mean
    '''
    diff = []
    for i in range(len(values_list) - 1):
        diff.append(abs(abs(values_list[i]) - abs(values_list[i + 1])))
    return np.mean(diff)


actuator_positions = [
    0.000,
    0.005,
    0.010,
    0.015,
    0.020,
    0.025,
    0.030,
    0.035,
    0.040,
    0.045,
    0.050,
]

bpm_phases_in_deg = [
    -85.9,
    -53.6,
    -21.0,
    12.6,
    46.2,
    78.0,
    111.6,
    145.0,
    178.4,
    -147.9,
    -114.9,
]
# Convert deg to radians so we can unwrap around -pi/+pi
bpm_phases_in_rad = [phase * (np.pi / 180.0) for phase in bpm_phases_in_deg]
unwrapped_bpm_phases = [
    (phase + np.pi) % (2 * np.pi) - np.pi for phase in bpm_phases_in_rad
]




# get the mean phase difference, and the mean actuator difference
mean_phase_diff  = get_average_relative_difference(unwrapped_bpm_phases)
mean_actuator_diff = get_average_relative_difference(actuator_positions)
print(f"{mean_phase_diff=} rad")
print(f"{mean_actuator_diff=} m")
# convert between phase and time using BPM FREQUENCY
mean_pulse_length = mean_phase_diff / BPM_FREQUENCY
# using distance travelled per actuator shift and phase shift
# to calculate velocity
average_velocity = mean_actuator_diff / mean_pulse_length
print(f"avg velocity: {average_velocity} m/s")
# using ke = .5mv^2 with known mass of proton with unit conversion to eV
energy = 0.5 * PROTON_MASS_KG * (average_velocity**2) * EV_PER_JOULE
print(f"particle energy: ", energy, "eV")
