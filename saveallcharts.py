from datachart import load_rainfall_data, plot_rainfall_for_year
import os
import matplotlib.pyplot as plt

xml_path = 'monthlyElement.xml'
out_dir = 'rainfall_charts'
years, _ = load_rainfall_data(xml_path)
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
for year in years:
    fig, ax = plot_rainfall_for_year(xml_path, year)
    out_path = os.path.join(out_dir, f'rainfall_{year}.png')
    fig.savefig(out_path)
    plt.close(fig)
    print(f'Saved: {out_path}')