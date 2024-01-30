from epics import caget, caput


class Corrector:
    def __init__(self, name: str):
        self.name = name

    @property
    def field_strength(self):
        return caget(self.name + ":B")

    @field_strength.setter
    def field_strength(self, strength: float):
        caput(self.name + ":B_Set", strength)
