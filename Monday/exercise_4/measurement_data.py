import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
from slit_scan import BEAM_PIPE_RADIUS_MM
from data_reader import get_positions, get_charges

FULL_SCAN_FILENAME = "scan_from_-50.0_to_50.0_with_400_steps.csv"
all_positions = get_positions(FULL_SCAN_FILENAME)
all_charges = get_charges(FULL_SCAN_FILENAME)

ACTIVE_SCAN_FILENAME = "scan_from_10.0_to_50.0_with_200_steps.csv"
active_positions = get_positions(ACTIVE_SCAN_FILENAME)
active_charges = get_charges(ACTIVE_SCAN_FILENAME)

#####
# Fit normal distribution to charge values 
# when slit is most active on beam
#####
mu, std = stats.norm.fit(active_charges)


#####
# Beam is intercepted by entire slit when charge is lowest
#####
min_charge_index = all_charges.index(min(all_charges))
intercept_position = all_positions[min_charge_index]
print(f"Beam is intercepted at: {intercept_position} mm")


slit_end_position = active_positions[-1]
slit_start_position = active_positions[0]
total_slit_distance = slit_end_position - slit_start_position
integrated_charge = float(np.sum(active_charges))/total_slit_distance
max_charge = max(all_charges)
slit_diff = active_positions[1] - active_positions[0]

#########
# the fraction of the beam (integrated charge/max_charge)
# is the same as the fraction of the slit position (delta)
# of the total slit distance
#########
slit_width = (integrated_charge / max_charge) * slit_diff
print('** Answers **')
print(f"Transverse RMS beam size: {mu} mm")
print(f"Beam position relative to slit: {BEAM_PIPE_RADIUS_MM - intercept_position} mm")
print(f"Slit width: {slit_width} mm")
