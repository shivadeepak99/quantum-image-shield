"""
Image Analysis Module

This module provides functions to analyze encryption quality through
various metrics including entropy, histogram uniformity, correlation,
and PSNR (Peak Signal-to-Noise Ratio).
"""

import numpy as np
from scipy.stats import entropy as scipy_entropy
import matplotlib.pyplot as plt
import io


def calculate_entropy(image_array):
    """
    Calculate Shannon entropy of an image.
    
    Higher entropy indicates better randomness and security.
    
    Args:
        image_array: 2D numpy array of pixel values
        
    Returns:
        float: Entropy value in bits
    """
    # Flatten image
    flat_image = image_array.flatten()
    
    # Calculate histogram (probability distribution)
    hist, _ = np.histogram(flat_image, bins=256, range=(0, 256))
    
    # Normalize to get probabilities
    probabilities = hist / len(flat_image)
    
    # Remove zero probabilities (log of 0 is undefined)
    probabilities = probabilities[probabilities > 0]
    
    # Calculate entropy using base 2 logarithm
    entropy_value = scipy_entropy(probabilities, base=2)
    
    return entropy_value


def calculate_histogram_uniformity(image_array):
    """
    Calculate histogram uniformity metric.
    
    A more uniform histogram (closer to 1) indicates better encryption.
    
    Args:
        image_array: 2D numpy array of pixel values
        
    Returns:
        float: Uniformity score (0 to 1)
    """
    # Flatten image
    flat_image = image_array.flatten()
    
    # Calculate histogram
    hist, _ = np.histogram(flat_image, bins=256, range=(0, 256))
    
    # Expected frequency for uniform distribution
    expected_freq = len(flat_image) / 256
    
    # Calculate chi-square statistic
    chi_square = np.sum((hist - expected_freq) ** 2 / expected_freq)
    
    # Normalize to 0-1 scale (lower chi-square = more uniform)
    # Use exponential decay for normalization
    uniformity = np.exp(-chi_square / (len(flat_image) * 10))
    
    return uniformity


def calculate_correlation(image_array, direction='horizontal'):
    """
    Calculate correlation between adjacent pixels.
    
    Lower correlation indicates better encryption.
    
    Args:
        image_array: 2D numpy array of pixel values
        direction: 'horizontal', 'vertical', or 'diagonal'
        
    Returns:
        float: Correlation coefficient (-1 to 1)
    """
    if direction == 'horizontal':
        x = image_array[:, :-1].flatten()
        y = image_array[:, 1:].flatten()
    elif direction == 'vertical':
        x = image_array[:-1, :].flatten()
        y = image_array[1:, :].flatten()
    elif direction == 'diagonal':
        x = image_array[:-1, :-1].flatten()
        y = image_array[1:, 1:].flatten()
    else:
        raise ValueError("Direction must be 'horizontal', 'vertical', or 'diagonal'")
    
    # Calculate correlation coefficient
    if len(x) > 0 and len(y) > 0:
        correlation = np.corrcoef(x, y)[0, 1]
    else:
        correlation = 0.0
    
    return correlation


def calculate_psnr(original_array, decrypted_array):
    """
    Calculate Peak Signal-to-Noise Ratio between original and decrypted images.
    
    Higher PSNR indicates better decryption quality.
    Infinity means perfect reconstruction.
    
    Args:
        original_array: 2D numpy array of original pixel values
        decrypted_array: 2D numpy array of decrypted pixel values
        
    Returns:
        float: PSNR value in dB (or inf for perfect match)
    """
    # Calculate Mean Squared Error
    mse = np.mean((original_array.astype(float) - decrypted_array.astype(float)) ** 2)
    
    if mse == 0:
        return float('inf')
    
    # Maximum possible pixel value
    max_pixel = 255.0
    
    # Calculate PSNR
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    
    return psnr


def generate_histogram_plot(image_array, title="Histogram"):
    """
    Generate a histogram plot for an image.
    
    Args:
        image_array: 2D numpy array of pixel values
        title: Title for the plot
        
    Returns:
        bytes: PNG image data of the histogram
    """
    plt.figure(figsize=(10, 4))
    plt.hist(image_array.flatten(), bins=256, range=(0, 256), color='blue', alpha=0.7)
    plt.title(title)
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return buf.getvalue()


def generate_correlation_plot(image_array, direction='horizontal', title="Correlation Plot", sample_size=5000):
    """
    Generate a scatter plot showing correlation between adjacent pixels.
    
    Args:
        image_array: 2D numpy array of pixel values
        direction: 'horizontal', 'vertical', or 'diagonal'
        title: Title for the plot
        sample_size: Number of pixel pairs to plot (for performance)
        
    Returns:
        bytes: PNG image data of the plot
    """
    if direction == 'horizontal':
        x = image_array[:, :-1].flatten()
        y = image_array[:, 1:].flatten()
    elif direction == 'vertical':
        x = image_array[:-1, :].flatten()
        y = image_array[1:, :].flatten()
    elif direction == 'diagonal':
        x = image_array[:-1, :-1].flatten()
        y = image_array[1:, 1:].flatten()
    else:
        raise ValueError("Direction must be 'horizontal', 'vertical', or 'diagonal'")
    
    # Sample for better visualization
    if len(x) > sample_size:
        indices = np.random.choice(len(x), sample_size, replace=False)
        x = x[indices]
        y = y[indices]
    
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, alpha=0.1, s=1)
    plt.title(title)
    plt.xlabel('Pixel value at position i')
    plt.ylabel('Pixel value at position i+1')
    plt.xlim(0, 255)
    plt.ylim(0, 255)
    plt.grid(True, alpha=0.3)
    
    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return buf.getvalue()


def analyze_image(image_array):
    """
    Perform comprehensive analysis on an image.
    
    Args:
        image_array: 2D numpy array of pixel values
        
    Returns:
        dict: Dictionary containing all analysis metrics
    """
    results = {
        'entropy': calculate_entropy(image_array),
        'uniformity': calculate_histogram_uniformity(image_array),
        'correlation_horizontal': calculate_correlation(image_array, 'horizontal'),
        'correlation_vertical': calculate_correlation(image_array, 'vertical'),
        'correlation_diagonal': calculate_correlation(image_array, 'diagonal'),
    }
    
    return results
