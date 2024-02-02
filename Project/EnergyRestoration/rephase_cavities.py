from calculate_energy import energy_from_bpm_phases
from pv_definitions import bpms_and_pv, cavities_and_pv
import time
SLEEP_TIME = 1.5
ON = 1.0
OFF = 0.0
cavities_and_pv['a']['AMP_SET'].put(OFF)
cavities_and_pv['b']['AMP_SET'].put(ON)
cavities_and_pv['c']['AMP_SET'].put(ON)
cavities_and_pv['d']['AMP_SET'].put(ON)

CAV_B_PHASE = -130.8
CAV_C_PHASE = -67.4
CAV_D_PHASE = 32.2

cavities_and_pv['b']['PHASE_SET'].put(CAV_B_PHASE)
cavities_and_pv['c']['PHASE_SET'].put(CAV_C_PHASE)
cavities_and_pv['d']['PHASE_SET'].put(CAV_D_PHASE)

time.sleep(SLEEP_TIME)

bpm23_phase = bpms_and_pv['BPM23']['PHASE'].get()
bpm32_phase = bpms_and_pv['BPM32']['PHASE'].get()

ENERGY_GUESS = 986e6

calculated_energy = energy_from_bpm_phases(bpm23_phase, bpm32_phase, ENERGY_GUESS)

print(f'{calculated_energy=}')