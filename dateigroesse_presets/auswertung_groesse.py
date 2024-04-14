import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Lese die Daten
work_path = os.path.dirname(os.path.realpath(__file__))
results_file = os.path.join(work_path, "results.csv")
df = pd.read_csv(results_file)

# Erstellen Sie ein gruppiertes Balkendiagramm
fig, ax = plt.subplots(figsize=(10, 6))

# Breite der Balken
bar_width = 0.2

# Eindeutige CRF-Werte und Presets
unique_crf = sorted(df['CRF'].unique())
unique_presets = df['Preset'].unique()

# Erzeugen einer Regenbogenfarbpalette
colors = plt.cm.nipy_spectral(np.linspace(0, 1, len(unique_presets)))

# Anzahl der Gruppen und der CRF-Werte
n_groups = len(unique_crf)
n_presets = len(unique_presets)

# Berechnung der Position der Balken
index = np.arange(n_groups) * (bar_width * n_presets + 0.3)  # Erhöhe den Abstand zwischen den Gruppen

for i, preset in enumerate(unique_presets):
    # Filtere die Daten für das aktuelle Preset
    preset_data = df[df['Preset'] == preset].sort_values(by='CRF')
    
    # Erzeuge Balken für Dateigröße
    ax.bar(index + i * bar_width, preset_data['FileSize'], bar_width, label=f'{preset}', color=colors[i])

# Anpassung der Achsenbeschriftungen und des Titels
ax.set_xlabel('CRF-Wert')
ax.set_ylabel('Dateigröße (MB)')
ax.set_title('Einfluss der Presets auf Dateigröße nach CRF-Wert')
ax.set_xticks(index + bar_width / 2 * (n_presets - 1))
ax.set_xticklabels(unique_crf)

# Legende hinzufügen
ax.legend()
plt.grid()
# Layout anpassen und speichern
plt.tight_layout()
plt.savefig(os.path.join(work_path, "crf_grouped_bar_chart.pdf"))
