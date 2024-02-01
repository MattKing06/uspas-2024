import yaml
from matplotlib import pyplot as plt
import numpy as np
amp_scan_data = {}
with open("amp_scan_data.yml", "r") as file:
    amp_scan_data = yaml.safe_load(file)

gradients = []
for amp_setting_label, data in amp_scan_data.items():
    plt.plot(data['RF_PHASES'], data['BPM_PHASES'], label=amp_setting_label)
    delta_y = data['BPM_PHASES'][-1] - data['BPM_PHASES'][0]
    delta_x = data['RF_PHASES'][-1] - data['RF_PHASES'][0]
    gradient = delta_y/delta_x
    print(amp_setting_label, ' Veff : ', gradient)
    gradients.append(gradient)

plt.title('Zero Crossing Phase Plot')
plt.xlabel('RF Phase [deg]')
plt.ylabel('BPM Phase [deg]')
plt.legend()
plt.show()
        