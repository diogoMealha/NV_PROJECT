# version 1.1
import os
import re
import pyarrow.parquet as pq
import plotly.express as px

# --- User-configurable settings ---
data_dir = "synthetic_parquet"   # Directory containing Parquet files
row_index = 100                   # Pixel row (0-based index)
col_index = 200                   # Pixel column (0-based index)

# Regex to extract frequency in MHz from filename (e.g., img_2870MHz.parquet)
pattern = re.compile(r"img_(\d+)MHz\.parquet$")

# Lists to hold frequency and intensity data
freqs = []
intensities = []

# Iterate sorted filenames for consistent ordering
for fname in sorted(os.listdir(data_dir)):
    print(fname)
    match = pattern.match(fname)
    if not match:
        continue
    mhz = int(match.group(1))
    freq_ghz = mhz / 1000.0

    # Read Parquet, convert to DataFrame
    path = os.path.join(data_dir, fname)
    table = pq.read_table(path)
    df = table.to_pandas()

    # Extract pixel intensity
    col_name = f"c{col_index}"
    intensity = df[col_name].iat[row_index]

    freqs.append(freq_ghz)
    intensities.append(intensity)

# Create interactive Plotly figure
fig = px.line(
    x=freqs,
    y=intensities,
    markers=True,
    labels={
        'x': 'Frequency (GHz)',
        'y': 'Pixel Intensity'
    },
    title=f"Pixel ({row_index}, {col_index}) Intensity vs Frequency"
)
fig.show()