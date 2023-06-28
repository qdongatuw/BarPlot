from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook


file = filedialog.askopenfilename()
wb = load_workbook(filename=file)
ws1 = wb['WT']
ws2 = wb['cKO']

data1_list = []
data2_list = []

for row in ws1.rows:
    data1_list.append([i.value for i in row])
for row in ws2.rows:
    data2_list.append([i.value for i in row])

x = np.linspace(0, 200, 5)
data1 = np.asarray(data1_list)
data2 = np.asarray(data2_list)
data1_mean = data1.mean(axis=0)
data1_sem = data1.std(axis=0)/(len(data1_list[0])**0.5)
data1_low = data1_mean - data1_sem
data1_high = data1_mean + data1_sem
data2_mean = data2.mean(axis=0)
data2_sem = data2.std(axis=0)/(len(data2_list[0])**0.5)
data2_low = data2_mean - data2_sem
data2_high = data2_mean + data2_sem
plt.plot(x, data1_mean, color='#222288', label='WT')
plt.plot(x, data2_mean, color='#882222', label='cKO')
plt.fill_between(x, data1_low, data1_high, color='#6666cc', alpha=0.5)
plt.fill_between(x, data2_low, data2_high, color='#cc6666', alpha=0.5)
plt.xlabel('Injected current (pA)')
plt.ylabel('Firing rate (Hz)')
plt.legend()
plt.show()
