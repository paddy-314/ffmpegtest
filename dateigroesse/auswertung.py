import matplotlib.pyplot as plt
import pandas as pd
import os

# Lese die Daten
work_path = os.path.dirname(os.path.realpath(__file__))
results_file = os.path.join(work_path, "results.csv")
df = pd.read_csv(results_file)

df = df[(df['CRF'] >= 17) & (df['CRF'] <= 28)]

# Farbschema und Beschriftungen für spezifische CRF-Werte definieren
color_labels = {
    17: ('green', 'Stadt'),
    23: ('blue', 'Land'),
    28: ('red', 'Offen')
}
# Fallback-Farbe für andere CRF-Werte
default_color = 'black'

# Farben und Labels für Balken basierend auf CRF-Werten zuordnen
bar_colors = [color_labels.get(crf, (default_color, 'Andere'))[0] for crf in df['CRF']]
bar_labels = [color_labels.get(crf, (default_color, 'Andere'))[1] for crf in df['CRF']]

fig, ax1 = plt.subplots()

# Balken für Dateigröße zeichnen
ax1.grid(axis='y')
bars = ax1.bar(df['CRF'], df['FileSize'], color=bar_colors, label='Dateigröße (MB)')
ax1.set_xlabel('CRF-Wert', color='black')
ax1.set_ylabel('Dateigröße (MB)', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Zweite Y-Achse für Bitrate
ax2 = ax1.twinx()
ax2.plot(df['CRF'], df['Bitrate'], color='tab:blue', marker='o', linestyle='-', label='Bitrate (Kbits/s)')
ax2.set_ylabel('Bitrate (Kbits/s)', color='black')
ax2.tick_params(axis='y', labelcolor='black')

# Legende für Balkenfarben erstellen
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color, edgecolor='black', label=label) for _, (color, label) in color_labels.items()]
legend_elements.append(Patch(facecolor=default_color, edgecolor='black', label='Andere CRF-Werte'))

# Gesamte Legende zusammenführen
handles, labels = ax2.get_legend_handles_labels()
plt.legend(handles=legend_elements + handles, loc='upper right', frameon=True)

plt.title('Einfluss des CRF-Wertes auf Dateigröße und Bitrate', color='black')
fig.tight_layout()

plt.savefig(os.path.join(work_path, "crf_stacked_barchart.pdf"))
