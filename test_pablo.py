import pickle
from ffpyplayer.pic import Image as FFPImage
import numpy as np
import matplotlib.pyplot as plt


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
print(pix_fmt)

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