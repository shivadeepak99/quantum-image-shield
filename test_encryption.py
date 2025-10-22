"""
Test script for Quantum-Seed ImageShield.

This script demonstrates the complete encryption/decryption workflow
and validates the implementation.
"""

import numpy as np
from quantum_key_generator import generate_quantum_key
from image_encryptor import (
    ImageEncryptor,
    load_image_as_grayscale,
    save_image_array
)
from image_analysis import (
    analyze_image,
    calculate_psnr
)


def test_encryption_decryption():
    """Test the complete encryption and decryption workflow."""
    
    print("=" * 60)
    print("Quantum-Seed ImageShield - Test Suite")
    print("=" * 60)
    
    # Load sample image
    print("\n1. Loading sample image...")
    try:
        original_image = load_image_as_grayscale('samples/sample_image.png')
        print(f"   ✓ Image loaded: {original_image.shape[1]}x{original_image.shape[0]} pixels")
    except FileNotFoundError:
        print("   ! Sample image not found. Generating...")
        from generate_sample_image import create_sample_image
        create_sample_image()
        original_image = load_image_as_grayscale('samples/sample_image.png')
        print(f"   ✓ Image loaded: {original_image.shape[1]}x{original_image.shape[0]} pixels")
    
    # Generate quantum keys
    print("\n2. Generating quantum keys...")
    image_size = original_image.size
    keystream, permutation_seed = generate_quantum_key(image_size, seed=42)
    print(f"   ✓ Keystream generated: {len(keystream)} bytes")
    print(f"   ✓ Permutation seed: {permutation_seed}")
    
    # Encrypt image
    print("\n3. Encrypting image...")
    encryptor = ImageEncryptor(keystream, permutation_seed)
    encrypted_image = encryptor.encrypt_image(original_image)
    print(f"   ✓ Image encrypted successfully")
    
    # Save encrypted image
    save_image_array(encrypted_image, 'samples/encrypted_image.png')
    print(f"   ✓ Encrypted image saved: samples/encrypted_image.png")
    
    # Decrypt image
    print("\n4. Decrypting image...")
    decrypted_image = encryptor.decrypt_image(encrypted_image)
    print(f"   ✓ Image decrypted successfully")
    
    # Save decrypted image
    save_image_array(decrypted_image, 'samples/decrypted_image.png')
    print(f"   ✓ Decrypted image saved: samples/decrypted_image.png")
    
    # Verify decryption
    print("\n5. Verifying decryption...")
    psnr = calculate_psnr(original_image, decrypted_image)
    is_perfect = np.array_equal(original_image, decrypted_image)
    
    if is_perfect:
        print(f"   ✓ Perfect reconstruction! PSNR = ∞")
        print(f"   ✓ Original and decrypted images are identical")
    else:
        print(f"   ✗ PSNR = {psnr:.2f} dB")
        print(f"   ✗ Warning: Decryption not perfect!")
    
    # Analyze images
    print("\n6. Analyzing images...")
    print("\n   Original Image Metrics:")
    original_metrics = analyze_image(original_image)
    print(f"      - Entropy: {original_metrics['entropy']:.4f} bits")
    print(f"      - Uniformity: {original_metrics['uniformity']:.4f}")
    print(f"      - Horizontal Correlation: {original_metrics['correlation_horizontal']:.4f}")
    print(f"      - Vertical Correlation: {original_metrics['correlation_vertical']:.4f}")
    print(f"      - Diagonal Correlation: {original_metrics['correlation_diagonal']:.4f}")
    
    print("\n   Encrypted Image Metrics:")
    encrypted_metrics = analyze_image(encrypted_image)
    print(f"      - Entropy: {encrypted_metrics['entropy']:.4f} bits")
    print(f"      - Uniformity: {encrypted_metrics['uniformity']:.4f}")
    print(f"      - Horizontal Correlation: {encrypted_metrics['correlation_horizontal']:.4f}")
    print(f"      - Vertical Correlation: {encrypted_metrics['correlation_vertical']:.4f}")
    print(f"      - Diagonal Correlation: {encrypted_metrics['correlation_diagonal']:.4f}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    entropy_increase = encrypted_metrics['entropy'] - original_metrics['entropy']
    avg_corr_original = np.mean([
        original_metrics['correlation_horizontal'],
        original_metrics['correlation_vertical'],
        original_metrics['correlation_diagonal']
    ])
    avg_corr_encrypted = np.mean([
        encrypted_metrics['correlation_horizontal'],
        encrypted_metrics['correlation_vertical'],
        encrypted_metrics['correlation_diagonal']
    ])
    corr_decrease = avg_corr_original - avg_corr_encrypted
    
    print(f"✓ Entropy increased by: {entropy_increase:.4f} bits")
    print(f"✓ Average correlation decreased by: {corr_decrease:.4f}")
    print(f"✓ Uniformity improved: {encrypted_metrics['uniformity'] > original_metrics['uniformity']}")
    
    if is_perfect:
        print(f"✓ Decryption: PERFECT ✓")
    else:
        print(f"✗ Decryption: FAILED")
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)
    
    return is_perfect


if __name__ == "__main__":
    success = test_encryption_decryption()
    exit(0 if success else 1)
