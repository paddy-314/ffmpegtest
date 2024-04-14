import matplotlib.pyplot as plt
import numpy as np
import os

work_path = os.path.dirname(os.path.realpath(__file__))
FILE_PREFIX = "times_"
y_vals_grouped = []

for i in range(1,4):
    path = os.path.join(work_path, f"{FILE_PREFIX}{i*10}s.txt")
    with open(path) as f:
        y_values = np.array([float(line.strip()) for line in f.readlines()])
        y_vals_grouped.append(y_values)

y_vals_mean = [y.mean() for y in y_vals_grouped]
x_values_grouped = np.arange(1, len(y_vals_grouped) + 1)

plt.ylim(0.4, 1.8)
# Plotting boxplots for each group of y-values to better utilize space and show distribution
plt.boxplot(y_vals_grouped, positions=x_values_grouped, widths=0.35, patch_artist=True, boxprops=dict(facecolor="lightblue"))

# Plotting the means as scatter points with a different marker for clarity
plt.scatter(x_values_grouped, y_vals_mean, color='green', zorder=5, label='Mittelwert', s=10, marker='x')

# Calculating and plotting a linear trend line for the means
z = np.polyfit(x_values_grouped, y_vals_mean, 1)
p = np.poly1d(z)
plt.plot(x_values_grouped, p(x_values_grouped), "r--", label='Linearer Trend')

# Adjusting plot details
plt.ylabel('Encoder Zeit [s]')
plt.xticks(x_values_grouped, ["10s", "20s", "30s"])
plt.title('Verteilung der Codierungszeiten (Beginn)')
plt.legend()

plt.tight_layout()  # Adjust layout to make room for the plot elements
plt.savefig(os.path.join(work_path, "boxplot_start.pdf"))

