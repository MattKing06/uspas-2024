import time
from epics import caget, caput
from matplotlib import pyplot as plt
import numpy as np
import csv

POSITION_TOLERANCE = 0.0001
slit_speed_pv = "slit:Speed_Set"
slit_destination_pv = "slit:Position_Set"
slit_position_pv = "slit:Position"
charge_pv = "FC:charge"
BEAM_PIPE_RADIUS_MM = 50
REFRESH_SPEED = 1 / caget(slit_speed_pv)


def perform_slit_scan_and_collect_charge_measurements(
    start_position: float = -50.0,
    end_position: float = 50.0,
    num_steps: int = 100,
    save_data: bool = True,
):
    charge_measurements = []
    position_readbacks = []
    target_positions = slit_target_positions = np.linspace(
        start_position,
        end_position,
        num_steps,
    )
    for position in target_positions:
        caput(slit_destination_pv, position)
        print(f"moving to {position}")
        while (
            abs(abs(caget(slit_position_pv)) - abs(caget(slit_destination_pv)))
            > POSITION_TOLERANCE
        ):
            time.sleep(REFRESH_SPEED)
        charge_measurements.append(caget(charge_pv))
        position_readbacks.append(caget(slit_position_pv))
    if save_data:
        filename = (
            f"scan_from_{start_position}_to_{end_position}_with_{num_steps}_steps.csv"
        )
        with open(filename, "w", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(("slit_position_mm", "f_cup_charge"))
            for i in zip(position_readbacks, charge_measurements):
                writer.writerow(i)
    return position_readbacks, charge_measurements


if __name__ == "__main__":
    positions, charge_measurements = perform_slit_scan_and_collect_charge_measurements(
        start_position=10.0,
        end_position=50.0,
        num_steps=200,
        save_data=True,
    )

    plt.scatter(positions, charge_measurements)
    plt.show()
