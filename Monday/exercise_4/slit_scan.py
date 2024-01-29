import time
from epics import caget, caput
from matplotlib import pyplot as plt
import numpy as np

POSITION_TOLERANCE = 0.0001
slit_speed_pv = 'slit:Speed_Set'
slit_destination_pv = 'slit:Position_Set'
slit_position_pv = 'slit:Position'
charge_pv = 'FC:charge'
BEAM_PIPE_RADIUS_MM = 50
REFRESH_SPEED = 1/caget(slit_speed_pv)

charge_measurements = []
slit_target_positions = np.linspace(10, 50, 40)
print(slit_target_positions)

for position in slit_target_positions:
    caput(slit_destination_pv, position)
    print(f'moving to {position}')
    while abs(abs(caget(slit_position_pv)) - abs(caget(slit_destination_pv))) > POSITION_TOLERANCE:
        time.sleep(REFRESH_SPEED)
    charge_measurements.append(caget(charge_pv))


measurments = [[slit_target_positions[i], charge_measurements[i]] for i in range(len(charge_measurements))]
print(measurments)
plt.plot(slit_target_positions, charge_measurements)
plt.show()