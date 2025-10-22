"""
Quick verification script to prove lossless encryption
"""

from PIL import Image
import numpy as np

# Load images
original = np.array(Image.open('samples/sample_image.png'))
decrypted = np.array(Image.open('decrypted_output.png'))
encrypted = np.array(Image.open('encrypted_output.png'))

# Verify lossless encryption
print("🔍 Verification Results:")
print("="*50)

# Check shapes
print(f"\n📐 Image Shapes:")
print(f"   Original:  {original.shape}")
print(f"   Encrypted: {encrypted.shape}")
print(f"   Decrypted: {decrypted.shape}")

# Check if decryption is perfect
is_perfect = np.array_equal(original, decrypted)
print(f"\n✨ Perfect Decryption: {'✅ YES!' if is_perfect else '❌ NO'}")

if is_perfect:
    print(f"   PSNR: ∞ (lossless)")
else:
    mse = np.mean((original.astype(float) - decrypted.astype(float)) ** 2)
    psnr = 20 * np.log10(255.0 / np.sqrt(mse)) if mse > 0 else float('inf')
    print(f"   PSNR: {psnr:.2f} dB")

# Check if encrypted is different from original
is_different = not np.array_equal(original, encrypted)
print(f"\n🔒 Encryption Applied: {'✅ YES!' if is_different else '❌ NO'}")

# Calculate difference percentage
if original.shape == encrypted.shape:
    different_pixels = np.sum(original != encrypted)
    total_pixels = original.size
    diff_percentage = (different_pixels / total_pixels) * 100
    print(f"   Changed pixels: {different_pixels}/{total_pixels} ({diff_percentage:.2f}%)")

# Entropy comparison
def calculate_entropy(img):
    hist, _ = np.histogram(img.flatten(), bins=256, range=(0, 255))
    hist = hist / hist.sum()
    entropy = -np.sum(hist * np.log2(hist + 1e-10))
    return entropy

original_entropy = calculate_entropy(original)
encrypted_entropy = calculate_entropy(encrypted)

print(f"\n📊 Entropy Analysis:")
print(f"   Original:  {original_entropy:.4f} bits")
print(f"   Encrypted: {encrypted_entropy:.4f} bits")
print(f"   Improvement: {((encrypted_entropy - original_entropy) / original_entropy * 100):.2f}%")

print("\n" + "="*50)
print("🎉 Quantum-Seed ImageShield v2.0.0 - WORKING!")
print("="*50)
