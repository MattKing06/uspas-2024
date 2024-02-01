# Positions of 1st gap and BPM (meters)
Pos_SCL_LLRF_FCM23a = 87.33689
Pos_SCL_LLRF_FCM23b = 88.78432
Pos_SCL_LLRF_FCM23c = 90.09974
Pos_SCL_LLRF_FCM23d = 91.54717
Pos_SCL_Diag_BPM23 = 93.662
Pos_SCL_Diag_BPM32 = 164.681
# Normal energies at cavity entrances (eV)
Energy_SCL_LLRF_FCM23a = 945.207e6
Energy_SCL_LLRF_FCM23d = 987.167e6
# BPM phase offsets (degrees)
Phi_Offset_SCL_Diag_BPM23 = 56.0608
Phi_Offset_SCL_Diag_BPM32 = -171.2920
# PV Names
from epics import PV

# Store cavity-name and PV objects for the Phase, Amp Setpoints
# in a dictionary.
cavities = ["a", "b", "c", "d"]
cavities_and_pv = {cavity: {} for cavity in cavities}
for cavity in cavities:
    cavities_and_pv[cavity].update({"AMP_SET": PV(f"SCL_LLRF:FCM23{cavity}:CtlAmpSet")})
    cavities_and_pv[cavity].update(
        {"PHASE_SET": PV(f"SCL_LLRF:FCM23{cavity}:CtlPhaseSet")}
    )

# Store BPM-name and PV objects for the Phase Readback
# in a dictionary.
bpms = ["BPM23", "BPM32"]
bpms_and_pv = {bpm: {} for bpm in bpms}
for name in bpms:
    bpms_and_pv[name].update({"PHASE": PV(f"SCL_Diag:{name}:phaseAvg")})
