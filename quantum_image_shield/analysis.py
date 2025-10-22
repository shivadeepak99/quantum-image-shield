"""
Image Analysis Module

Provides statistical analysis tools for evaluating image encryption quality.
Includes entropy calculation, histogram analysis, correlation metrics, and PSNR.
"""

import numpy as np
from typing import Dict, Tuple


def calculate_entropy(image_array: np.ndarray) -> float:
    """
    Calculate Shannon entropy of an image.
    
    Higher entropy indicates more randomness/information content.
    For encrypted images, we want entropy close to 8 bits (maximum for 8-bit images).
    
    Args:
        image_array: 2D numpy array of pixel values (0-255)
        
    Returns:
        Entropy in bits (0-8 for 8-bit images)
    """
    # Flatten the image
    flat_image = image_array.flatten()
    
    # Calculate histogram
    hist, _ = np.histogram(flat_image, bins=256, range=(0, 256))
    
    # Calculate probabilities (remove zero counts)
    hist = hist[hist > 0]
    probabilities = hist / hist.sum()
    
    # Calculate entropy
    entropy = -np.sum(probabilities * np.log2(probabilities))
    
    return entropy


def calculate_histogram_uniformity(image_array: np.ndarray) -> float:
    """
    Calculate histogram uniformity score.
    
    Measures how uniform the pixel distribution is.
    Score of 1.0 = perfectly uniform (ideal for encrypted images)
    Score near 0 = very non-uniform
    
    Args:
        image_array: 2D numpy array of pixel values
        
    Returns:
        Uniformity score (0-1)
    """
    # Calculate histogram
    hist, _ = np.histogram(image_array.flatten(), bins=256, range=(0, 256))
    
    # Ideal uniform distribution
    ideal_count = image_array.size / 256
    
    # Calculate chi-square statistic
    chi_square = np.sum((hist - ideal_count) ** 2 / ideal_count)
    
    # Normalize to 0-1 score (lower chi-square = more uniform)
    # Max chi-square for completely non-uniform distribution
    max_chi_square = image_array.size - 256
    uniformity = 1 - (chi_square / max_chi_square) if max_chi_square > 0 else 1
    
    return max(0, min(1, uniformity))


def calculate_correlation(image_array: np.ndarray, direction: str = 'horizontal') -> float:
    """
    Calculate pixel correlation in a given direction.
    
    Low correlation indicates good encryption (pixels are independent).
    
    Args:
        image_array: 2D numpy array of pixel values
        direction: 'horizontal', 'vertical', or 'diagonal'
        
    Returns:
        Correlation coefficient (-1 to 1)
    """
    if direction == 'horizontal':
        # Compare each pixel with its right neighbor
        x = image_array[:, :-1].flatten()
        y = image_array[:, 1:].flatten()
    elif direction == 'vertical':
        # Compare each pixel with its bottom neighbor
        x = image_array[:-1, :].flatten()
        y = image_array[1:, :].flatten()
    elif direction == 'diagonal':
        # Compare each pixel with its bottom-right neighbor
        x = image_array[:-1, :-1].flatten()
        y = image_array[1:, 1:].flatten()
    else:
        raise ValueError("Direction must be 'horizontal', 'vertical', or 'diagonal'")
    
    # Calculate correlation coefficient
    if len(x) == 0:
        return 0.0
    
    correlation = np.corrcoef(x, y)[0, 1]
    
    return correlation if not np.isnan(correlation) else 0.0


def calculate_psnr(original: np.ndarray, reconstructed: np.ndarray) -> float:
    """
    Calculate Peak Signal-to-Noise Ratio between two images.
    
    PSNR measures reconstruction quality:
    - Infinity = perfect reconstruction
    - >40 dB = excellent quality
    - 30-40 dB = good quality
    - <30 dB = poor quality
    
    Args:
        original: Original image array
        reconstructed: Reconstructed image array
        
    Returns:
        PSNR in decibels (dB)
    """
    # Check if images are identical
    if np.array_equal(original, reconstructed):
        return float('inf')
    
    # Calculate Mean Squared Error
    mse = np.mean((original.astype(float) - reconstructed.astype(float)) ** 2)
    
    if mse == 0:
        return float('inf')
    
    # Maximum possible pixel value
    max_pixel = 255.0
    
    # Calculate PSNR
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    
    return psnr


def analyze_image(image_array: np.ndarray) -> Dict[str, float]:
    """
    Perform comprehensive statistical analysis on an image.
    
    Args:
        image_array: 2D numpy array of pixel values
        
    Returns:
        Dictionary containing all analysis metrics
    """
    metrics = {
        'entropy': calculate_entropy(image_array),
        'uniformity': calculate_histogram_uniformity(image_array),
        'correlation_horizontal': calculate_correlation(image_array, 'horizontal'),
        'correlation_vertical': calculate_correlation(image_array, 'vertical'),
        'correlation_diagonal': calculate_correlation(image_array, 'diagonal'),
    }
    
    return metrics


def generate_histogram_plot(image_array: np.ndarray):
    """
    Generate a histogram plot for an image.
    
    Args:
        image_array: 2D numpy array of pixel values
        
    Returns:
        Matplotlib figure object
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("matplotlib is required for plotting. Install with: pip install matplotlib")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate histogram
    hist, bins = np.histogram(image_array.flatten(), bins=256, range=(0, 256))
    
    # Plot histogram
    ax.bar(bins[:-1], hist, width=1, color='blue', alpha=0.7)
    ax.set_xlabel('Pixel Value')
    ax.set_ylabel('Frequency')
    ax.set_title('Pixel Value Distribution')
    ax.grid(True, alpha=0.3)
    
    return fig


def generate_correlation_plot(image_array: np.ndarray, direction: str = 'horizontal', 
                              sample_size: int = 5000):
    """
    Generate a scatter plot showing pixel correlation.
    
    Args:
        image_array: 2D numpy array of pixel values
        direction: 'horizontal', 'vertical', or 'diagonal'
        sample_size: Number of pixel pairs to sample (for performance)
        
    Returns:
        Matplotlib figure object
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("matplotlib is required for plotting. Install with: pip install matplotlib")
    
    # Get pixel pairs based on direction
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
    
    # Sample for performance if dataset is large
    if len(x) > sample_size:
        indices = np.random.choice(len(x), sample_size, replace=False)
        x = x[indices]
        y = y[indices]
    
    # Create scatter plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(x, y, alpha=0.1, s=1)
    ax.set_xlabel(f'Pixel value at position i')
    ax.set_ylabel(f'Pixel value at adjacent position ({direction})')
    ax.set_title(f'{direction.capitalize()} Pixel Correlation')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    
    # Calculate and display correlation
    corr = calculate_correlation(image_array, direction)
    ax.text(0.05, 0.95, f'Correlation: {corr:.4f}', 
            transform=ax.transAxes, fontsize=12,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    return fig
