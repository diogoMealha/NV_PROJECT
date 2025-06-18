import pickle
import numpy as np
from ffpyplayer.pic import Image as FFPImage


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


def downsample_average(arr, block_size):
    """
    Downsamples a 2D array by averaging over non-overlapping grid blocks.

    Parameters:
        arr (np.ndarray): 2D input array (e.g., image).
        block_size (tuple): (block_rows, block_cols) size to average over.

    Returns:
        np.ndarray: Downsampled array.
    """
    r, c = arr.shape
    br, bc = block_size

    # Compute new size that fits whole blocks
    new_r = (r // br) * br
    new_c = (c // bc) * bc

    # Crop the array
    arr_cropped = arr[:new_r, :new_c]

    # Reshape into blocks and average
    reshaped = arr_cropped.reshape(new_r // br, br, new_c // bc, bc)
    downsampled = reshaped.mean(axis=(1, 3))

    return downsampled

def downsample_max(arr, block_size):
    """
    Downsamples a 2D array by averaging over non-overlapping grid blocks.

    Parameters:
        arr (np.ndarray): 2D input array (e.g., image).
        block_size (tuple): (block_rows, block_cols) size to average over.

    Returns:
        np.ndarray: Downsampled array.
    """
    r, c = arr.shape
    br, bc = block_size

    # Compute new size that fits whole blocks
    new_r = (r // br) * br
    new_c = (c // bc) * bc

    # Crop the array
    arr_cropped = arr[:new_r, :new_c]

    # Reshape into blocks and average
    reshaped = arr_cropped.reshape(new_r // br, br, new_c // bc, bc)
    downsampled = reshaped.max(axis=(1, 3))

    return downsampled


def random_uniform_dist_array(size, low, high):
    """
    Generates a random array with a uniform distribution.

    Parameters:
        size (tuple): Shape of the output array.
        low (float): Lower bound of the uniform distribution.
        high (float): Upper bound of the uniform distribution.

    Returns:
        np.ndarray: Randomly generated array.
    """
    return np.random.randint(low, high, size=size)





##### transformations we want to apply to the image
def apply_transformations(arr):
    max_value = np.max(arr)
    min_value = np.min(arr)
    # define a minimum threshold to count
    THRESHOLD_PERCENTAGE = 0.6
    THRESHOLD = (max_value - min_value) * THRESHOLD_PERCENTAGE + min_value # 
    arr[arr < THRESHOLD] = min_value

    return downsample_average(arr, (5, 5))  # Downsample the image
