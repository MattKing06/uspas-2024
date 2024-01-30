import time
from BPM import BPM
from Corrector import Corrector
from typing import List
from matplotlib import pyplot as plt


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
    """
    This script is the start of the home work where you
    have to close 3-kickers bump using DCV01, DCV04,
    and DCV05 correctors in MEBT.

    It shows how to create PV names and communicate with
    the Virtual Accelerator.

    >virtual_accelerator --debug  --sequences MEBT

    """
    # ---- set DCV01 t0 field 0.05 [T]
    correctors[0].field_strength = initial_strength

    # ---- give the accelerator time to put beam through MEBT
    time.sleep(2.0)
    # -------------------------------------------------
    # ---- Let's print BPM signals before bump closing
    # -------------------------------------------------
    print("======= BPMs before Closing =====")
    for bpm in bpms:
        print("BPM PV=", bpm.name, " y_avg[mm] = %+12.5g " % bpm.y_average)
    print("=================================")
    return [bpm.y_average for bpm in bpms]


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
    while abs(bpms_y[0] - bpms_y[-1]) > acceptance_tolerance:
        for c_index, corrector in enumerate(correctors[1:]):
            # set the field strength to the bpm-delta
            corrector.field_strength = delta_bpms_y[c_index]
            time.sleep(2)
            print("======= BPMs after iteration =====")
            for b_index, bpm in enumerate(bpms):
                delta_bpms_y[b_index] = bpms_y[b_index] - delta_bpms_y[b_index]
                bpms_y[b_index] = bpm.y_average
            [print(f"{bpm.name} y_avg[mm] = {bpm.y_average}") for bpm in bpms]
            print("=================================")
    print("======= BPMs after Closing =====")
    for bpm in bpms:
        print("BPM PV=", bpm.name, " y_avg[mm] = %+12.5g " % bpm.y_average)
    print("=================================")
    return [bpm.y_average for bpm in bpms], [
        corrector.field_strength for corrector in correctors
    ]


if __name__ == "__main__":
    correctors = setup_correctors()
    bpms = setup_bpms()
    initial_bpm_y = set_initial_orbit(
        correctors=correctors,
        bpms=bpms,
        initial_strength=0.05,
    )
    plt.plot([i for i in range(len(initial_bpm_y))], initial_bpm_y)
    plt.xlabel("BPM index [units]")
    plt.ylabel("BPM Y Average readback [mm]")
    plt.show()
    plt.show()
    final_bpm_y, final_corr_b = perform_orbit_kick(
        correctors=correctors,
        bpms=bpms,
        acceptance_tolerance=0.005,
    )
    plt.plot([i for i in range(len(final_bpm_y))], final_bpm_y)
    plt.xlabel("BPM index [units]")
    plt.ylabel("BPM Y Average readback [mm]")
    plt.show()
    for i, corrector in enumerate(correctors):
        print(f"Corrector {i} Value: {correctors[i].field_strength}")
