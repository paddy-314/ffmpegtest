import matplotlib.pyplot as plt
import os
import numpy as np

work_path = os.path.dirname(os.path.realpath(__file__))
FILE_PREFIX = "times_"
y_vals_mean = []

for i in range(1,4):
    path = os.path.join(work_path, f"{FILE_PREFIX}{i*10}s.txt")
    with open(path) as f:
        y_values = np.array([float(line.strip()) for line in f.readlines()])
        y_vals_mean.append(y_values.mean())
        x_values = [i]*len(y_values)
        plt.scatter(x_values, y_values, marker='.', alpha=0.1)

x_values = np.arange(1, len(y_vals_mean) + 1)
z = np.polyfit(x_values, y_vals_mean, 1)
p = np.poly1d(z)

plt.scatter(x_values, y_vals_mean, s=10, label="Mittelwert")
plt.plot(x_values, p(x_values), "r--", label='Linearer Trend')

plt.xlabel('Experiment Number')
plt.ylabel('Values (ms)')
plt.xticks(x_values) 
plt.legend()
plt.savefig(os.path.join(work_path, "linear_colorized.pdf"))
