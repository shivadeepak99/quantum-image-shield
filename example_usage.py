"""
Example Usage Script for Quantum-Seed ImageShield

This script demonstrates various use cases and API patterns.
"""

import numpy as np
from quantum_key_generator import QuantumKeyGenerator, generate_quantum_key
from image_encryptor import (
    ImageEncryptor,
    load_image_as_grayscale,
    save_image_array
)
from image_analysis import (
    calculate_entropy,
    calculate_histogram_uniformity,
    calculate_correlation,
    calculate_psnr,
    analyze_image
)


def example_1_basic_encryption():
    """Example 1: Basic encryption and decryption."""
    print("\n" + "="*60)
    print("Example 1: Basic Encryption/Decryption")
    print("="*60)
    
    # Load image
    print("Loading image...")
    original = load_image_as_grayscale('samples/sample_image.png')
    print(f"Image size: {original.shape}")
    
    # Generate quantum keys
    print("Generating quantum keys...")
    keystream, permutation_seed = generate_quantum_key(original.size, seed=42)
    print(f"Keystream length: {len(keystream)}")
    print(f"Permutation seed: {permutation_seed}")
    
    # Encrypt
    print("Encrypting...")
    encryptor = ImageEncryptor(keystream, permutation_seed)
    encrypted = encryptor.encrypt_image(original)
    
    # Decrypt
    print("Decrypting...")
    decrypted = encryptor.decrypt_image(encrypted)
    
    # Verify
    is_identical = np.array_equal(original, decrypted)
    print(f"Decryption successful: {is_identical}")
    
    return encrypted, decrypted


def example_2_custom_key_generator():
    """Example 2: Using QuantumKeyGenerator class directly."""
    print("\n" + "="*60)
    print("Example 2: Custom Key Generator")
    print("="*60)
    
    # Create key generator
    generator = QuantumKeyGenerator(seed=123)
    
    # Generate different types of keys
    print("Generating various keys...")
    
    # Generate random bits
    random_bits = generator.generate_random_bits(32)
    print(f"Random bits (32): {random_bits[:16]}...")
    
    # Generate keystream
    keystream = generator.generate_keystream(100)
    print(f"Keystream (100 bytes): {keystream[:10]}...")
    
    # Generate permutation seed
    perm_seed = generator.generate_permutation_seed()
    print(f"Permutation seed: {perm_seed}")


def example_3_analysis_metrics():
    """Example 3: Detailed analysis of encryption quality."""
    print("\n" + "="*60)
    print("Example 3: Encryption Quality Analysis")
    print("="*60)
    
    # Load images
    original = load_image_as_grayscale('samples/sample_image.png')
    keystream, seed = generate_quantum_key(original.size, seed=42)
    encryptor = ImageEncryptor(keystream, seed)
    encrypted = encryptor.encrypt_image(original)
    decrypted = encryptor.decrypt_image(encrypted)
    
    # Calculate individual metrics
    print("\nOriginal Image:")
    print(f"  Entropy: {calculate_entropy(original):.4f} bits")
    print(f"  Uniformity: {calculate_histogram_uniformity(original):.4f}")
    print(f"  Horizontal Correlation: {calculate_correlation(original, 'horizontal'):.4f}")
    print(f"  Vertical Correlation: {calculate_correlation(original, 'vertical'):.4f}")
    print(f"  Diagonal Correlation: {calculate_correlation(original, 'diagonal'):.4f}")
    
    print("\nEncrypted Image:")
    print(f"  Entropy: {calculate_entropy(encrypted):.4f} bits")
    print(f"  Uniformity: {calculate_histogram_uniformity(encrypted):.4f}")
    print(f"  Horizontal Correlation: {calculate_correlation(encrypted, 'horizontal'):.4f}")
    print(f"  Vertical Correlation: {calculate_correlation(encrypted, 'vertical'):.4f}")
    print(f"  Diagonal Correlation: {calculate_correlation(encrypted, 'diagonal'):.4f}")
    
    print("\nDecryption Quality:")
    psnr = calculate_psnr(original, decrypted)
    if np.isinf(psnr):
        print(f"  PSNR: ∞ dB (Perfect reconstruction)")
    else:
        print(f"  PSNR: {psnr:.2f} dB")


def example_4_batch_processing():
    """Example 4: Process multiple images with the same keys."""
    print("\n" + "="*60)
    print("Example 4: Batch Processing (Single Image Demo)")
    print("="*60)
    
    # In a real scenario, you might have multiple images
    # For this demo, we'll use the same image but demonstrate the pattern
    
    images = {
        'image1': 'samples/sample_image.png',
    }
    
    # Generate keys once
    print("Generating quantum keys...")
    # Determine the size (assuming all images are the same size)
    first_image = load_image_as_grayscale(images['image1'])
    keystream, seed = generate_quantum_key(first_image.size, seed=999)
    
    # Create encryptor
    encryptor = ImageEncryptor(keystream, seed)
    
    # Process each image
    for name, path in images.items():
        print(f"\nProcessing {name}...")
        original = load_image_as_grayscale(path)
        encrypted = encryptor.encrypt_image(original)
        decrypted = encryptor.decrypt_image(encrypted)
        
        # Verify
        is_perfect = np.array_equal(original, decrypted)
        print(f"  Encryption: ✓")
        print(f"  Decryption: {'✓' if is_perfect else '✗'}")


def example_5_security_assessment():
    """Example 5: Comprehensive security assessment."""
    print("\n" + "="*60)
    print("Example 5: Security Assessment")
    print("="*60)
    
    # Load and encrypt image
    original = load_image_as_grayscale('samples/sample_image.png')
    keystream, seed = generate_quantum_key(original.size, seed=777)
    encryptor = ImageEncryptor(keystream, seed)
    encrypted = encryptor.encrypt_image(original)
    
    # Analyze both images
    original_analysis = analyze_image(original)
    encrypted_analysis = analyze_image(encrypted)
    
    # Calculate improvements
    print("\nSecurity Metrics Improvements:")
    
    entropy_gain = encrypted_analysis['entropy'] - original_analysis['entropy']
    print(f"  Entropy gain: {entropy_gain:+.4f} bits ({entropy_gain/original_analysis['entropy']*100:+.2f}%)")
    
    uniformity_gain = encrypted_analysis['uniformity'] - original_analysis['uniformity']
    print(f"  Uniformity gain: {uniformity_gain:+.4f} ({uniformity_gain/original_analysis['uniformity']*100:+.2f}%)")
    
    avg_corr_orig = np.mean([
        original_analysis['correlation_horizontal'],
        original_analysis['correlation_vertical'],
        original_analysis['correlation_diagonal']
    ])
    avg_corr_enc = np.mean([
        encrypted_analysis['correlation_horizontal'],
        encrypted_analysis['correlation_vertical'],
        encrypted_analysis['correlation_diagonal']
    ])
    corr_reduction = avg_corr_orig - avg_corr_enc
    print(f"  Avg correlation reduction: {corr_reduction:+.4f} ({corr_reduction/avg_corr_orig*100:+.2f}%)")
    
    # Security assessment
    print("\nSecurity Assessment:")
    
    checks = []
    checks.append(("High entropy (>7.5 bits)", encrypted_analysis['entropy'] > 7.5))
    checks.append(("Uniform histogram (>0.9)", encrypted_analysis['uniformity'] > 0.9))
    checks.append(("Low correlation (<0.1)", abs(avg_corr_enc) < 0.1))
    checks.append(("Entropy increased", entropy_gain > 0))
    
    for check_name, passed in checks:
        print(f"  {'✓' if passed else '✗'} {check_name}")
    
    all_passed = all(passed for _, passed in checks)
    print(f"\nOverall: {'SECURE ✓' if all_passed else 'NEEDS IMPROVEMENT'}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Quantum-Seed ImageShield - Example Usage")
    print("="*60)
    
    try:
        example_1_basic_encryption()
        example_2_custom_key_generator()
        example_3_analysis_metrics()
        example_4_batch_processing()
        example_5_security_assessment()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60)
        
    except FileNotFoundError:
        print("\n⚠ Error: Sample image not found.")
        print("Please run: python generate_sample_image.py")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
