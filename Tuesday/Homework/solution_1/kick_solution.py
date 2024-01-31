import time
from BPM import BPM
from Corrector import Corrector
from typing import List
from matplotlib import pyplot as plt
import numpy as np


def setup_bpms() -> List[BPM]:
    # ---- BPM01, BPM04, BPM05, BPM10, and BPM11
    bpm_ind_arr = ["01", "04", "05", "10", "11", "14"]
    bpms = []
    for index in bpm_ind_arr:
        bpms.append(BPM("MEBT_Diag:BPM" + index))
    return bpms


def setup_correctors() -> List[Corrector]:
    # make correctors
    dcv_ind_arr = ["01", "04", "05", "10", "11", "14"]
    correctors = []
    for index in dcv_ind_arr:
        # ---- put 0. [T] field in all DCV
        corrector = Corrector("MEBT_Mag:PS_DCV" + str(index))
        corrector.field_strength = 0.0
        correctors.append(corrector)
    return correctors


def set_initial_orbit(
    correctors: List[Corrector], bpms: List[BPM], initial_strength: float
) -> None:
    # ---- set DCV01 t0 field 0.05 [T]
    correctors[0].field_strength = initial_strength

    # ---- give the accelerator time to put beam through MEBT
    time.sleep(2.0)
    # -------------------------------------------------
    # ---- Let's print BPM signals before bump closing
    # -------------------------------------------------
    print("======= BPMs before Closing =====")
    print_bpm_status(bpms)
    print("=================================")
    return [bpm.y_average for bpm in bpms]


def print_bpm_status(bpms: List[BPM]):
    [print(f"{bpm.name} y_avg[mm] = {bpm.y_average}") for bpm in bpms]


def perform_orbit_kick(
    correctors: List[Corrector],
    bpms: List[BPM],
    acceptance_tolerance: float,
):
    bpms_y = [bpm.y_average for bpm in bpms]
    delta_bpms_y = [0.0] * len(bpms_y)
    # keep changing strengths until difference
    # between the first and last bpm y-value are within
    # the defined tolerance
    while abs(abs(bpms_y[0]) - abs(bpms_y[-1])) >= acceptance_tolerance:
        for c_index, corrector in enumerate(correctors[1:]):
            # set the field strength to the bpm-delta
            corrector.field_strength = delta_bpms_y[c_index]
            time.sleep(2)
            for b_index, bpm in enumerate(bpms):
                # calculate delta y's after b-field change
                delta_bpms_y[b_index] = bpms_y[b_index] - delta_bpms_y[b_index]
                # record new bpm y
                bpms_y[b_index] = bpm.y_average
            print("======= BPMs after iteration =====")
            print_bpm_status(bpms)
            print("=================================")
    print("======= BPMs after Closing =====")
    print_bpm_status(bpms)
    print("=================================")
    return [bpm.y_average for bpm in bpms], [
        corrector.field_strength for corrector in correctors
    ]


"""
This script is the start of the home work where you
have to close 3-kickers bump using DCV01, DCV04,
and DCV05 correctors in MEBT.

It shows how to create PV names and communicate with
the Virtual Accelerator.

>virtual_accelerator --debug  --sequences MEBT

"""
if __name__ == "__main__":
    initial_strengths = [0.01, 0.05, 0.07]
    for strength in initial_strengths:
        correctors = setup_correctors()
        bpms = setup_bpms()
        initial_bpm_y = set_initial_orbit(
            correctors=correctors,
            bpms=bpms,
            initial_strength=strength,
        )
        bpm_names = [bpms[i].name for i in range(len(initial_bpm_y))]
        fig_pre = plt.figure()
        plt.plot(bpm_names, initial_bpm_y)
        plt.xlabel("BPM")
        plt.ylabel("BPM Y Average readback [mm]")
        plt.title(
            f"Initial BPM Positions through lattice (initial corrector strength: {strength} [T])"
        )
        final_bpm_y, final_corr_b = perform_orbit_kick(
            correctors=correctors,
            bpms=bpms,
            acceptance_tolerance=0.005,
        )
        fig_post = plt.figure()
        plt.plot(bpm_names, final_bpm_y)
        plt.xlabel("BPM")
        plt.ylabel("BPM Y Average readback [mm]")
        plt.title(
            f"Final BPM Positions through lattice (initial corrector strength: {strength} [T])"
        )
        plt.show()
        for i, corrector in enumerate(correctors):
            print(f"{corrector.name} Strength[T] = {correctors[i].field_strength}")
