"""
Generate a sample test image for demonstration.
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np


def create_sample_image():
    """Create a sample grayscale image with text and patterns."""
    # Create a new grayscale image
    width, height = 256, 256
    image = Image.new('L', (width, height), color=255)
    draw = ImageDraw.Draw(image)
    
    # Add some geometric patterns
    # Draw gradient background
    for y in range(height):
        intensity = int(255 * (1 - y / height))
        draw.line([(0, y), (width, y)], fill=intensity)
    
    # Draw some shapes
    draw.rectangle([50, 50, 100, 100], fill=0, outline=0)
    draw.ellipse([120, 50, 200, 130], fill=100, outline=100)
    draw.polygon([(30, 150), (80, 200), (10, 220)], fill=200, outline=200)
    
    # Add text
    try:
        # Try to add text (may not work without font)
        draw.text((70, 180), "QUANTUM", fill=0)
        draw.text((60, 200), "IMAGE SHIELD", fill=0)
    except:
        # If font fails, just add more patterns
        draw.rectangle([60, 180, 190, 220], fill=50, outline=50)
    
    # Save the image
    image.save('samples/sample_image.png')
    print("Sample image created: samples/sample_image.png")
    print(f"Size: {width}x{height} pixels")
    
    return image


if __name__ == "__main__":
    create_sample_image()
