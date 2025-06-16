import pickle
from ffpyplayer.pic import Image as FFPImage
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os
import pyarrow as pa
import pyarrow.parquet as pq

def load_frame_from_pickle(path: str) -> 'ffpyplayer.pic.Image':
    with open(path, 'rb') as f:
        data = pickle.load(f)

    # 3) rebuild the ffpyplayer.pic.Image
    img = FFPImage(
        data['planes'],
        pix_fmt   = data['pix_fmt'],
        size      = data['size'],

    )
    return img

img2 = load_frame_from_pickle('obj2.bn')

# now extract arr and pixfmt:
buf = img2.to_bytearray()[0]
width, height = img2.get_size()
data = np.frombuffer(buf, dtype='<u2')   # uint16 little‐endian
arr = data.reshape((height, width))
pixfmt = img2.get_pixel_format()         # e.g. 'gray16le'
# ——————————————————————————————

# display
plt.imshow(arr, cmap='gray', vmin=arr.min(), vmax=arr.max())
plt.axis('off')
plt.show()

out_dir = "synthetic_parquet"
os.makedirs(out_dir, exist_ok=True)

# build frequency list: 0 MHz baseline, then 2.80 → 2.95 GHz in 1 MHz steps
freqs = np.concatenate((
    [0.0],
    np.arange(2.80, 2.95 + 0.001, 0.001)
))

# Lorentzian dip parameters
f0    = 2.87    # GHz
gamma = 0.005   # FWHM (~5 MHz)
A     = 0.3     # max fractional dip

def lorentzian(f):
    return 1.0 / (1.0 + ((f - f0)/(gamma/2))**2)

H, W = arr.shape
averages = []

for f in freqs:
    if f == 0.0:
        synth = arr
    else:
        dip    = A * lorentzian(f)
        factor = 1.0 - dip
        synth  = (arr.astype(np.float32) * factor).clip(0, np.iinfo(arr.dtype).max)
        synth  = synth.astype(arr.dtype)

    # record average
    averages.append((f, float(synth.mean())))

    # build Arrow table: one column per image column
    cols  = [pa.array(synth[:, i]) for i in range(W)]
    names = [f"c{i}" for i in range(W)]
    tbl   = pa.Table.from_arrays(cols, names=names)

    # attach metadata
    meta = {
        b"pixelformat": pixfmt.encode("utf-8"),
        b"frequency":   f"{f:.3f}GHz".encode("utf-8"),
    }
    tbl = tbl.replace_schema_metadata(meta)

    # write parquet
    fname = f"img_{int(f*1000):04d}MHz.parquet"
    pq.write_table(tbl, os.path.join(out_dir, fname), compression="snappy")
    print(f"Wrote {fname}")

# save averages to CSV
import csv
with open(os.path.join(out_dir, "averages.csv"), "w", newline="") as cf:
    w = csv.writer(cf)
    w.writerow(["frequency_GHz", "avg_pixel"])
    w.writerows(averages)

