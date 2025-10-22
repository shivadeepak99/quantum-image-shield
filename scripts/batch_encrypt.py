"""
Batch Image Encryption Tester
Usage: python batch_encrypt.py <folder_path>
"""

import sys
import os
from pathlib import Path
from quantum_image_shield import ImageEncryptor, ImageDecryptor
from quantum_image_shield.validators import ImageValidator
from PIL import Image
import numpy as np

def test_image(image_path: str, purity: str = 'balanced'):
    """Test encryption/decryption on a single image."""
    
    print(f"\n{'='*60}")
    print(f"🔐 Testing: {Path(image_path).name}")
    print(f"{'='*60}")
    
    # Validate image
    print("1️⃣ Validating image...")
    is_valid, error, img = ImageValidator.validate_image_file(image_path)
    if not is_valid:
        print(f"   ❌ Validation failed: {error}")
        return False
    
    img_array = np.array(img)
    img.close()
    print(f"   ✅ Valid image: {img_array.shape}, mode: {Image.open(image_path).mode}")
    
    # Encrypt
    print(f"2️⃣ Encrypting with '{purity}' purity...")
    encryptor = ImageEncryptor(quantum_purity=purity)
    encrypted_array = encryptor.encrypt_array(img_array)
    xor_key, perm_key = encryptor.get_last_keys()
    print(f"   ✅ Encrypted! XOR key: {len(xor_key)} bytes, Permutation: {len(perm_key)} elements")
    
    # Decrypt
    print("3️⃣ Decrypting...")
    decryptor = ImageDecryptor()
    decrypted_array = decryptor.decrypt_array(encrypted_array, xor_key, perm_key)
    print(f"   ✅ Decrypted!")
    
    # Verify
    print("4️⃣ Verifying lossless encryption...")
    is_lossless = np.array_equal(img_array, decrypted_array)
    
    if is_lossless:
        print("   ✅ PERFECT! Lossless encryption verified (PSNR = ∞)")
    else:
        mse = np.mean((img_array.astype(float) - decrypted_array.astype(float)) ** 2)
        psnr = 20 * np.log10(255.0 / np.sqrt(mse)) if mse > 0 else float('inf')
        print(f"   ⚠️ PSNR: {psnr:.2f} dB")
    
    # Stats
    changed_pixels = np.sum(img_array != encrypted_array)
    total_pixels = img_array.size
    change_percent = (changed_pixels / total_pixels) * 100
    
    print(f"5️⃣ Encryption stats:")
    print(f"   • Pixels changed: {changed_pixels}/{total_pixels} ({change_percent:.2f}%)")
    
    # Entropy
    def calc_entropy(arr):
        hist, _ = np.histogram(arr.flatten(), bins=256, range=(0, 255))
        hist = hist / hist.sum()
        return -np.sum(hist * np.log2(hist + 1e-10))
    
    orig_entropy = calc_entropy(img_array)
    enc_entropy = calc_entropy(encrypted_array)
    
    print(f"   • Entropy: {orig_entropy:.4f} → {enc_entropy:.4f} bits")
    print(f"   • Improvement: {((enc_entropy - orig_entropy) / orig_entropy * 100):.2f}%")
    
    print(f"\n{'✅ TEST PASSED!' if is_lossless else '⚠️ TEST WARNING'}")
    return is_lossless


def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_encrypt.py <image_file_or_folder>")
        print("\nExamples:")
        print("  python batch_encrypt.py myimage.png")
        print("  python batch_encrypt.py C:\\Users\\YourName\\Pictures")
        print("  python batch_encrypt.py samples")
        return
    
    path = sys.argv[1]
    purity = sys.argv[2] if len(sys.argv) > 2 else 'balanced'
    
    # Check if path exists
    if not os.path.exists(path):
        print(f"❌ Path not found: {path}")
        return
    
    # Supported formats
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'}
    
    # Get list of images
    images = []
    if os.path.isfile(path):
        images = [path]
    elif os.path.isdir(path):
        for file in Path(path).rglob('*'):
            if file.suffix.lower() in image_extensions:
                images.append(str(file))
    
    if not images:
        print(f"❌ No images found in: {path}")
        return
    
    print(f"\n🔮 Quantum-Seed ImageShield - Batch Test")
    print(f"{'='*60}")
    print(f"Found {len(images)} image(s)")
    print(f"Quantum purity: {purity}")
    print(f"{'='*60}")
    
    # Test each image
    passed = 0
    failed = 0
    
    for img_path in images:
        try:
            result = test_image(img_path, purity)
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Error testing {img_path}: {e}")
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Total:  {len(images)}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
