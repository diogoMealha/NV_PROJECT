import pickle
from ffpyplayer.pic import Image as FFPImage
import numpy as np
import matplotlib.pyplot as plt
import csv


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

# --- usage ---pip

# later when you need it back:
img2 = load_frame_from_pickle('obj2.bn')


pix_fmt = img2.get_pixel_format()
#print(pix_fmt)

# get raw bytes and dimensions
buf = img2.to_bytearray()[0]
width, height = img2.get_size()

# interpret as little-endian 16-bit grayscale
data = np.frombuffer(buf, dtype='<u2')   # uint16, little-endian
arr = data.reshape((height, width))

# display
plt.imshow(arr, cmap='gray', vmin=arr.min(), vmax=arr.max())
plt.axis('off')
plt.show()


pixfmt    = img2.get_pixel_format()  # e.g. 'gray16le'

if False:
    with open('snapshot.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        # 1st three lines: metadata
        writer.writerow(['pixelformat', pixfmt])
        writer.writerow(['timestamp',    "2023-10-01T12:00:00Z"])  # example timestamp
        writer.writerow(['time_base',    "timebase_example"])  # example timebase

        # now write the pixel values
        # each row of the image becomes one CSV row
        for row in arr:
            writer.writerow(row.tolist())