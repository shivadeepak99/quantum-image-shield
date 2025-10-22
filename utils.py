# utils.py
import numpy as np
from PIL import Image
import cv2
from typing import Tuple
from math import log2

def load_grayscale(path: str) -> np.ndarray:
    """Load an image and return a 2D numpy uint8 array (grayscale).
    Accepts color images and converts to grayscale.
    """
    img = Image.open(path).convert('L')
    arr = np.array(img, dtype=np.uint8)
    return arr

def save_grayscale(arr: np.ndarray, path: str):
    img = Image.fromarray(arr.astype(np.uint8), mode='L')
    img.save(path)

def flatten(img: np.ndarray) -> np.ndarray:
    return img.flatten()

def reshape(flat: np.ndarray, shape: Tuple[int, int]) -> np.ndarray:
    return flat.reshape(shape)

def image_entropy(img: np.ndarray) -> float:
    """Calculate Shannon entropy of a grayscale image (base-2).
    Returns entropy in bits per pixel.
    """
    hist, _ = np.histogram(img.flatten(), bins=256, range=(0, 255))
    probs = hist / hist.sum()
    probs = probs[probs > 0]
    return -(probs * np.log2(probs)).sum()

def adjacent_pixel_correlation(img: np.ndarray) -> dict:
    """Compute correlation coefficients for adjacent pixels in horizontal, vertical, and diagonal directions.
    Returns a dict with keys 'horizontal', 'vertical', 'diagonal'.
    """
    arr = img.astype(np.float64)
    h, w = arr.shape

    def corr(x, y):
        x = x.flatten()
        y = y.flatten()
        mx = x.mean()
        my = y.mean()
        num = ((x - mx) * (y - my)).sum()
        den = np.sqrt(((x - mx) ** 2).sum() * ((y - my) ** 2).sum())
        if den == 0:
            return 0.0
        return num / den

    # horizontal pairs (i, j) and (i, j+1)
    h1 = arr[:, :-1]
    h2 = arr[:, 1:]
    horizontal = corr(h1, h2)

    # vertical
    v1 = arr[:-1, :]
    v2 = arr[1:, :]
    vertical = corr(v1, v2)

    # diagonal (down-right)
    d1 = arr[:-1, :-1]
    d2 = arr[1:, 1:]
    diagonal = corr(d1, d2)

    return {'horizontal': horizontal, 'vertical': vertical, 'diagonal': diagonal}

def histogram_flatness(img: np.ndarray) -> np.ndarray:
    """Return histogram counts (256 bins).
    """
    hist, _ = np.histogram(img.flatten(), bins=256, range=(0, 255))
    return hist

def psnr(original: np.ndarray, reconstructed: np.ndarray) -> float:
    """Peak signal-to-noise ratio between two grayscale images.
    If identical, returns float('inf').
    """
    mse = np.mean((original.astype(np.float64) - reconstructed.astype(np.float64)) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse))
