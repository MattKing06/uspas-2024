from epics import caget


class BPM:
    def __init__(self, name: str):
        self.name = name

    @property
    def x_average(self) -> float:
        return caget(self.name + ":xAvg")

    @property
    def y_average(self) -> float:
        return caget(self.name + ":yAvg")
