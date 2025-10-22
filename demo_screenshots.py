"""
Generate demonstration screenshots and visualizations for the project.
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from image_encryptor import load_image_as_grayscale
from image_analysis import generate_histogram_plot, generate_correlation_plot
import io


def create_demo_visualization():
    """Create a comprehensive demo visualization."""
    
    # Load images
    original = load_image_as_grayscale('samples/sample_image.png')
    encrypted = load_image_as_grayscale('samples/encrypted_image.png')
    decrypted = load_image_as_grayscale('samples/decrypted_image.png')
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(18, 12))
    
    # Row 1: Images
    ax1 = plt.subplot(3, 3, 1)
    ax1.imshow(original, cmap='gray')
    ax1.set_title('Original Image', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    ax2 = plt.subplot(3, 3, 2)
    ax2.imshow(encrypted, cmap='gray')
    ax2.set_title('Encrypted Image', fontsize=14, fontweight='bold')
    ax2.axis('off')
    
    ax3 = plt.subplot(3, 3, 3)
    ax3.imshow(decrypted, cmap='gray')
    ax3.set_title('Decrypted Image', fontsize=14, fontweight='bold')
    ax3.axis('off')
    
    # Row 2: Histograms
    ax4 = plt.subplot(3, 3, 4)
    ax4.hist(original.flatten(), bins=256, range=(0, 256), color='blue', alpha=0.7)
    ax4.set_title('Original Histogram', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Pixel Value')
    ax4.set_ylabel('Frequency')
    ax4.grid(True, alpha=0.3)
    
    ax5 = plt.subplot(3, 3, 5)
    ax5.hist(encrypted.flatten(), bins=256, range=(0, 256), color='red', alpha=0.7)
    ax5.set_title('Encrypted Histogram', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Pixel Value')
    ax5.set_ylabel('Frequency')
    ax5.grid(True, alpha=0.3)
    
    ax6 = plt.subplot(3, 3, 6)
    ax6.hist(decrypted.flatten(), bins=256, range=(0, 256), color='green', alpha=0.7)
    ax6.set_title('Decrypted Histogram', fontsize=12, fontweight='bold')
    ax6.set_xlabel('Pixel Value')
    ax6.set_ylabel('Frequency')
    ax6.grid(True, alpha=0.3)
    
    # Row 3: Correlation plots
    ax7 = plt.subplot(3, 3, 7)
    x_orig = original[:, :-1].flatten()
    y_orig = original[:, 1:].flatten()
    sample_size = 5000
    if len(x_orig) > sample_size:
        indices = np.random.choice(len(x_orig), sample_size, replace=False)
        x_orig = x_orig[indices]
        y_orig = y_orig[indices]
    ax7.scatter(x_orig, y_orig, alpha=0.1, s=1, color='blue')
    ax7.set_title('Original Correlation', fontsize=12, fontweight='bold')
    ax7.set_xlabel('Pixel at position i')
    ax7.set_ylabel('Pixel at position i+1')
    ax7.grid(True, alpha=0.3)
    
    ax8 = plt.subplot(3, 3, 8)
    x_enc = encrypted[:, :-1].flatten()
    y_enc = encrypted[:, 1:].flatten()
    if len(x_enc) > sample_size:
        indices = np.random.choice(len(x_enc), sample_size, replace=False)
        x_enc = x_enc[indices]
        y_enc = y_enc[indices]
    ax8.scatter(x_enc, y_enc, alpha=0.1, s=1, color='red')
    ax8.set_title('Encrypted Correlation', fontsize=12, fontweight='bold')
    ax8.set_xlabel('Pixel at position i')
    ax8.set_ylabel('Pixel at position i+1')
    ax8.grid(True, alpha=0.3)
    
    ax9 = plt.subplot(3, 3, 9)
    x_dec = decrypted[:, :-1].flatten()
    y_dec = decrypted[:, 1:].flatten()
    if len(x_dec) > sample_size:
        indices = np.random.choice(len(x_dec), sample_size, replace=False)
        x_dec = x_dec[indices]
        y_dec = y_dec[indices]
    ax9.scatter(x_dec, y_dec, alpha=0.1, s=1, color='green')
    ax9.set_title('Decrypted Correlation', fontsize=12, fontweight='bold')
    ax9.set_xlabel('Pixel at position i')
    ax9.set_ylabel('Pixel at position i+1')
    ax9.grid(True, alpha=0.3)
    
    plt.suptitle('Quantum-Seed ImageShield - Complete Workflow', fontsize=18, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    
    # Save the figure
    plt.savefig('samples/demo_visualization.png', dpi=150, bbox_inches='tight')
    print("✓ Demo visualization saved: samples/demo_visualization.png")
    plt.close()


if __name__ == "__main__":
    create_demo_visualization()
