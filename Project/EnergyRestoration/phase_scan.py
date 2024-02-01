"""
This script is the start of the home work where you
will scan a phase of the last MEBT re-buncher RF caity
to find the non-accelerating phase and the cavity amplitude.

>virtual_accelerator --debug  --sequences MEBT

"""

import os
import sys
import math
import time

import numpy as np
import matplotlib.pyplot as plt

from epics import pv as pv_channel

from orbit.py_linac.linac_parsers import SNS_LinacLatticeFactory
from orbit.py_linac.lattice import MarkerLinacNode
from orbit.utils import phaseNearTargetPhaseDeg

from orbit.core.orbit_utils import Function
from orbit.utils.fitting import PolynomialFit

from uspas_pylib.harmonic_data_fitting_lib import fitCosineFunc, CosFittingScorer

# -------------------------------------------------------------------
#              START of the SCRIPT
# -------------------------------------------------------------------

# -----Parameters at the entrance of MEBT ---------------
# transverse emittances are unnormalized and in pi*mm*mrad
# longitudinal emittance is in pi*eV*sec
e_kin_ini = 0.0025  # in [GeV]
mass = 0.939294  # in [GeV]
gamma = (mass + e_kin_ini) / mass
beta = math.sqrt(gamma * gamma - 1.0) / gamma
print("relat. gamma=", gamma)
print("relat.  beta=", beta)
bpm_frequency = 805.0e6  # MHz
v_light = 2.99792458e8  # in [m/sec]

# -----------------------------------------------------------------
# ---- Let's switch off all cavities between cav_index and end
# -----------------------------------------------------------------
# for ind in range(cav_index + 1, len(rf_cavs) - 1):
#     cav_amp_pv_tmp = pv_channel.PV("MEBT_LLRF:FCM" + str(ind + 1) + ":CtlAmpSet")
#     cav_amp_pv_tmp.put(0.0)

# ------------------------------------------------------------------
# ---- Now we perform a phase scan measuring BPM phase
# ------------------------------------------------------------------
# cav_phase_pv = pv_channel.PV("MEBT_LLRF:FCM" + str(cav_index + 1) + ":CtlPhaseSet")
# cav_amp_pv = pv_channel.PV("MEBT_LLRF:FCM" + str(cav_index + 1) + ":CtlAmpSet")
# bpm_phase_pv = pv_channel.PV("MEBT_Diag:BPM14:phaseAvg")
# bpm_amp_pv = pv_channel.PV("MEBT_Diag:BPM14:amplitudeAvg")

import yaml
from pv_definitions import bpms_and_pv, cavities_and_pv


def do_scan_without_cavity_a():
    # set initial cavity-d
    initial_d_phase = -28.1536
    cavities_and_pv["d"]["PHASE_SET"].put(initial_d_phase)
    [pvs["AMP_SET"].put(0.0) for _, pvs in cavities_and_pv.items()]
    time.sleep(1.1)
    [print(_, pvs["AMP_SET"].get()) for _, pvs in cavities_and_pv.items()]
    # turn A on
    scan_data = {"scans": {}}
    for cavity, pvs in cavities_and_pv.items():
        if cavity == "a":
            continue
        initial_cavity_phase = pvs["PHASE_SET"].get()
        scan_data["scans"].update({cavity: {}})
        print(f"Turn Cavity {cavity} On")
        pvs["AMP_SET"].put(1.0)
        print(f"Phase Scan for Cavity {cavity}")
        phase_scan_data = do_phase_scan(cavity)
        scan_data["scans"].update({cavity: phase_scan_data})
        print(scan_data)
        bpm_min_index = phase_scan_data["BPM_PHASES"]["BPM32"].index(
            min(phase_scan_data["BPM_PHASES"]["BPM32"])
        )
        accelerating_phase = phase_scan_data["RF_PHASES"][bpm_min_index]
        pvs["PHASE_SET"].put(accelerating_phase)
        time.sleep(1.1)
    with open("all_cavity_phase_scans.yml", "w") as file:
        yaml.safe_dump(scan_data, file)


def do_all_cavity_scan():
    # set initial cavity-d
    initial_d_phase = -28.1536
    cavities_and_pv["d"]["PHASE_SET"].put(initial_d_phase)
    [pvs["AMP_SET"].put(0.0) for _, pvs in cavities_and_pv.items()]
    time.sleep(1.1)
    [print(_, pvs["AMP_SET"].get()) for _, pvs in cavities_and_pv.items()]
    # turn A on
    scan_data = {"scans": {}}
    for cavity, pvs in cavities_and_pv.items():
        initial_cavity_phase = pvs["PHASE_SET"].get()
        scan_data["scans"].update({cavity: {}})
        print(f"Turn Cavity {cavity} On")
        pvs["AMP_SET"].put(1.0)
        time.sleep(0.6)
        print(f"Phase Scan for Cavity {cavity}")
        phase_scan_data = do_phase_scan(cavity)
        scan_data["scans"].update({cavity: phase_scan_data})
        print(scan_data)
        pvs["PHASE_SET"].put(initial_cavity_phase)
        time.sleep(0.6)
    with open("all_cavity_phase_scans_unwrapped.yml", "w") as file:
        yaml.safe_dump(scan_data, file)


def do_phase_scan(cavity_name):
    phase_scan_values = range(-180, 182, 2)
    phase_scan_data = {}
    phase_scan_data["RF_PHASES"] = []
    phase_scan_data["RF_AMPLITUDE"] = []
    phase_scan_data["BPM_PHASES"] = {}

    for phase in phase_scan_values:
        cavities_and_pv[cavity_name]["PHASE_SET"].put(phase)
        print(f"Phase Set {phase}")
        time.sleep(0.6)
        phase_scan_data["RF_PHASES"].append(
            cavities_and_pv[cavity_name]["PHASE_SET"].get()
        )
        phase_scan_data["RF_AMPLITUDE"].append(
            cavities_and_pv[cavity_name]["AMP_SET"].get()
        )
        for bpm, pvs in bpms_and_pv.items():
            if bpm not in phase_scan_data["BPM_PHASES"]:
                phase_scan_data["BPM_PHASES"].update({bpm: []})
            phase_scan_data["BPM_PHASES"][bpm].append(pvs["PHASE"].get())
            phase_scan_data["BPM_PHASES"][bpm] =np.ndarray.tolist(np.rad2deg(np.unwrap(np.deg2rad(phase_scan_data["BPM_PHASES"][bpm]))))
    return phase_scan_data


if __name__ == "__main__":
    do_all_cavity_scan()
