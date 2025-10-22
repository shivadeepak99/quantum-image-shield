#!/usr/bin/env python3
"""Quick verification test after cleanup"""
from PIL import Image
import numpy as np

# Load images
original = Image.open("samples/sample_image.png")
encrypted = Image.open("test_encrypted.png")
decrypted = Image.open("test_decrypted.png")

# Convert to arrays
orig_arr = np.array(original)
enc_arr = np.array(encrypted)
dec_arr = np.array(decrypted)

# Verify lossless
is_lossless = np.array_equal(orig_arr, dec_arr)

# Calculate encryption stats
total_pixels = orig_arr.size
changed_pixels = np.sum(orig_arr != enc_arr)
change_rate = (changed_pixels / total_pixels) * 100

# Entropy
def calculate_entropy(img_array):
    values, counts = np.unique(img_array, return_counts=True)
    probabilities = counts / img_array.size
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
    return entropy

orig_entropy = calculate_entropy(orig_arr)
enc_entropy = calculate_entropy(enc_arr)

print("=" * 60)
print("🔐 QUANTUM ENCRYPTION TEST RESULTS")
print("=" * 60)
print(f"\n✅ Lossless Recovery: {is_lossless}")
print(f"   Original vs Decrypted: {'PERFECT MATCH ✨' if is_lossless else 'MISMATCH! ⚠️'}")
print(f"\n📊 Encryption Quality:")
print(f"   Pixels Changed: {change_rate:.2f}%")
print(f"   Original Entropy: {orig_entropy:.4f} bits")
print(f"   Encrypted Entropy: {enc_entropy:.4f} bits")
print(f"   Entropy Gain: +{((enc_entropy - orig_entropy) / orig_entropy * 100):.2f}%")
print(f"\n🎯 Status: {'🔥 ENCRYPTION WORKING PERFECTLY!' if is_lossless and change_rate > 99 else '⚠️ ISSUES DETECTED'}")
print("=" * 60)
