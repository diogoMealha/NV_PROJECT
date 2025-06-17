import pickle
from ffpyplayer.pic import Image as FFPImage
import numpy as np
import matplotlib.pyplot as plt
import csv
import utils.functions_file as ff


def load_frame_from_pickle(path: str) -> 'ffpyplayer.pic.Image':
    with open(path, 'rb') as f:
        data = pickle.load(f)

    # 3) rebuild the ffpyplayer.pic.Image
    print(data['planes'])
    print(type(data['planes']))
    img = FFPImage(
        data['planes'],
        pix_fmt   = data['pix_fmt'], # string: gray16le
        size      = data['size'], # tuple (2448, 2048)

    )
    return img

# --- usage ---pip

# later when you need it back:
NAME = 'obj2.bn'  # replace with your actual file name
img2 = load_frame_from_pickle(NAME)


pix_fmt = img2.get_pixel_format()
#print(pix_fmt)

# get raw bytes and dimensions
buf = img2.to_bytearray()[0]
width, height = img2.get_size()

# interpret as little-endian 16-bit grayscale
data = np.frombuffer(buf, dtype='<u2')   # uint16, little-endian
arr = data.reshape((height, width))

# image info
max_value = np.max(arr)
max_value_count = np.sum(arr == max_value)
min_value = np.min(arr)
min_value_count = np.sum(arr == min_value)
print(f"Max value: {max_value} Count: {max_value_count}")
print(f"Min value: {min_value} Count: {min_value_count}")


SIZE = (6, 6)
# display
plt.figure(figsize=SIZE)
plt.imshow(arr, cmap='gray', vmin=arr.min(), vmax=arr.max())
plt.axis('off')
plt.show()

# display

# image modifications - thresholding
# THRESHOLD = (max_value - min_value) * 0.6 + min_value
# arr[arr < THRESHOLD] = min_value

# image modifications - downsampling
# arr =ff.downsample_average(arr, (25, 25)) 
# THRESHOLD = (max_value - min_value) * 0.6 + min_value
# arr[arr < THRESHOLD] = min_value
# arr =ff.downsample_max(arr, (10, 10))  

arr_2 = ff.random_uniform_dist_array(arr.shape, np.min(arr), np.max(arr))

plt.figure(figsize=SIZE)
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