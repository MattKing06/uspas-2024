"""
This script is the start of the home work where you
have to close 3-kickers bump using DCV01, DCV04, 
and DCV05 correctors in MEBT.

It shows how to create PV names and communicate with 
the Virtual Accelerator.

>virtual_accelerator --debug  --sequences MEBT

"""

import sys
import math
import time

from epics import pv as pv_channel

# -------------------------------------------------------------------
#              START of the SCRIPT
# -------------------------------------------------------------------

# ---- DCV01, DCV04, DCV05, DCV10, DCV11, DCV14
from BPM import BPM
from Corrector import Corrector

# make correctors
dcv_ind_arr = ["01", "04", "05", "10", "11", "14"]
correctors = []
for index in dcv_ind_arr:
    # ---- put 0. [T] field in all DCV
    corrector = Corrector("MEBT_Mag:PS_DCV" + str(index)).field_strength = 0.0
    correctors.append(corrector)


# ---- set DCV01 t0 field 0.05 [T]
dcv01_field = 0.05
correctors[0].field_strength = dcv01_field

# ---- give the accelerator time to put beam through MEBT
time.sleep(2.0)

# ---- BPM01, BPM04, BPM05, BPM10, and BPM11
bpm_ind_arr = ["01", "04", "05", "10", "11", "14"]
bpms = []
for index in bpm_ind_arr:
    bpms.append(BPM("MEBT_Diag:BPM" + index))
# -------------------------------------------------
# ---- Let's print BPM signals before bump closing
# -------------------------------------------------
print("======= BPMs before Closing =====")
for bpm in bpms:
    print("BPM PV=", bpm.name, " y_avg[mm] = %+12.5g " % bpm.y_average)
print("=================================")
