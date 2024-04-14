import matplotlib.pyplot as plt
import os
import numpy as np

work_path = os.path.dirname(os.path.realpath(__file__))
FILE_PREFIX = "results"
y_values = []

for i in range(1,4):
    path = os.path.join(work_path, f"{FILE_PREFIX}{i*10}s.txt")
    with open(path) as f:
        y_values.append(float(f.readline().split()[1])*1000 - 50)

x_values = np.arange(1, len(y_values) + 1)
z = np.polyfit(x_values, y_values, 1)
p = np.poly1d(z)

plt.scatter(x_values, y_values, label='Data Points', marker='x', c='green')
plt.plot(x_values, p(x_values), "r--", label='Linear Trend Line')

plt.xlabel('Experiment Number')
plt.ylabel('Values (ms)')
plt.xticks(x_values) 
plt.savefig(os.path.join(work_path, "linear_summarized.pdf"))
