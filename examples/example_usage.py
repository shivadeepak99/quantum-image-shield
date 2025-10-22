"""
Example usage of Quantum-Seed ImageShield

This script demonstrates how to use the quantum-classical image encryption system.
"""

import sys
import os
import numpy as np
from PIL import Image

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantum_image_shield import QuantumKeyGenerator, ImageEncryptor, ImageDecryptor


def create_sample_image(filename="sample_image.png", size=(256, 256)):
    """Create a simple sample image for demonstration."""
    # Create a gradient image
    img_array = np.zeros((size[0], size[1], 3), dtype=np.uint8)
    for i in range(size[0]):
        for j in range(size[1]):
            img_array[i, j] = [i % 256, j % 256, (i + j) % 256]
    
    img = Image.fromarray(img_array, 'RGB')
    img.save(filename)
    print(f"Sample image created: {filename}")
    return filename


def main():
    """Demonstrate the encryption and decryption process."""
    print("=" * 60)
    print("Quantum-Seed ImageShield - Example Usage")
    print("=" * 60)
    print()
    
    # Step 1: Create a sample image
    print("Step 1: Creating a sample image...")
    input_image = create_sample_image()
    print()
    
    # Step 2: Encrypt the image
    print("Step 2: Encrypting the image with quantum-generated keys...")
    encryptor = ImageEncryptor(quantum_seed=42)  # Using seed for reproducibility
    
    encrypted_image = "encrypted_image.png"
    key_file = "encryption_keys.npz"
    
    xor_key, permutation_key = encryptor.encrypt_image(
        input_image,
        encrypted_image,
        key_file
    )
    
    print(f"  ✓ Original image: {input_image}")
    print(f"  ✓ Encrypted image saved: {encrypted_image}")
    print(f"  ✓ Keys saved: {key_file}")
    print(f"  ✓ XOR key length: {len(xor_key)} bytes")
    print(f"  ✓ Permutation size: {len(permutation_key)} elements")
    print()
    
    # Step 3: Decrypt the image
    print("Step 3: Decrypting the image...")
    decryptor = ImageDecryptor()
    
    decrypted_image = "decrypted_image.png"
    
    decryptor.decrypt_image(
        encrypted_image,
        decrypted_image,
        key_path=key_file
    )
    
    print(f"  ✓ Decrypted image saved: {decrypted_image}")
    print()
    
    # Step 4: Verify the decryption
    print("Step 4: Verifying decryption accuracy...")
    original = np.array(Image.open(input_image))
    decrypted = np.array(Image.open(decrypted_image))
    
    if np.array_equal(original, decrypted):
        print("  ✓ SUCCESS: Decrypted image matches the original perfectly!")
    else:
        print("  ✗ ERROR: Decrypted image does not match the original")
        difference = np.sum(np.abs(original.astype(int) - decrypted.astype(int)))
        print(f"  Total pixel difference: {difference}")
    print()
    
    # Step 5: Demonstrate quantum key generation
    print("Step 5: Demonstrating quantum key generation...")
    qkg = QuantumKeyGenerator()
    
    # Generate some random bits
    random_bits = qkg.generate_random_bits(16)
    print(f"  16 quantum random bits: {random_bits}")
    
    # Generate a random key
    random_key = qkg.generate_key(8)
    print(f"  8-byte quantum random key: {random_key.hex()}")
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
