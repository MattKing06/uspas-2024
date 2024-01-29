from matplotlib import pyplot as plt
BPM_FREQUENCY = 402.5e6
PROTON_MASS_KG = 1.67262192e-27
EV_PER_JOULE = 1/1.60218e-19
actuator_positions = [0.000,
0.005, 
0.010, 
0.015, 
0.020, 
0.025, 
0.030, 
0.035, 
0.040, 
0.045, 
0.050] 

bpm_phases_in_deg = [-85.9,
-53.6,
-21.0,
12.6,
46.2,
78.0,
111.6,
145.0,
178.4,
-147.9,
-114.9]

def get_relative_difference(values_list: list[float]):
    diff = []
    for i in range(len(values_list) - 1):
        diff.append(abs(abs(values_list[i])-abs(values_list[i+1])))
    return diff

phase_diff = get_relative_difference(bpm_phases_in_deg)
actuator_diff = get_relative_difference(actuator_positions)
mean_phase_diff = (sum(phase_diff)/len(phase_diff))
mean_actuator_diff = sum(actuator_diff)/len(actuator_diff)
print(mean_phase_diff)
phase_diff_per_actuator_position = mean_phase_diff/mean_actuator_diff
print(phase_diff_per_actuator_position)
average_velocity = phase_diff_per_actuator_position
print(average_velocity)
energy = .5*PROTON_MASS_KG*(average_velocity**2)
print(energy*EV_PER_JOULE)