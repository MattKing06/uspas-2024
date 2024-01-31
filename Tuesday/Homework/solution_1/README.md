Before running `kick_solution.py` make sure that you have activated the environment for [uspas24-CR](https://github.com/azukov/uspas24-CR.git).

This will allow you to run the virtual_accelerator by doing
```
virtual_accelerator --debug --sequences MEBT
```

After the virtual accelerator is running, you can run the `kick_solution.py` by doing `python kick_solution.py`. This script will perform a empircal kick to close the orbit using BPM readings.

The BPM class in `BPM.py` and Corrector class in `Corrector.py` have been made to move away from accessing PVs directly in `kick_solution.py`