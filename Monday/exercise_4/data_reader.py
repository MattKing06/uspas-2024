import csv
import os

SLIT_POSITION_KEY = 'slit_position_mm'
CHARGE_KEY = 'f_cup_charge'


def get_positions(filename: str):
    if not os.path.exists(filename):
        print(f"Could not find data file {filename}")
        return None
    with open(filename) as file:
        data = csv.DictReader(file, delimiter='\t')
        # creating empty lists
        positions = []
        # iterating over each row and append
        # values to empty list
        for col in data:
            positions.append(float(col[SLIT_POSITION_KEY]))
        return positions


def get_charges(filename: str):
    if not os.path.exists(filename):
        print(f"Could not find data file {filename}")
        return None
    with open(filename) as file:
        data = csv.DictReader(file, delimiter='\t')
        # creating empty lists
        charges = []
        # iterating over each row and append
        # values to empty list
        for col in data:
            charges.append(float(col[CHARGE_KEY]))
        return charges
