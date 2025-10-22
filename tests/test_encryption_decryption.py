"""
Tests for Image Encryption and Decryption modules
"""

import unittest
import numpy as np
from PIL import Image
import os
import tempfile
from quantum_image_shield.encryption import ImageEncryptor
from quantum_image_shield.decryption import ImageDecryptor


class TestEncryptionDecryption(unittest.TestCase):
    """Test cases for ImageEncryptor and ImageDecryptor classes."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_image_path = os.path.join(self.temp_dir, 'test_image.png')
        self.encrypted_path = os.path.join(self.temp_dir, 'encrypted.png')
        self.decrypted_path = os.path.join(self.temp_dir, 'decrypted.png')
        self.key_path = os.path.join(self.temp_dir, 'keys.npz')
        
        # Create a simple test image
        img_array = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)
        img = Image.fromarray(img_array, 'RGB')
        img.save(self.test_image_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary files
        for filename in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, filename))
        os.rmdir(self.temp_dir)
    
    def test_encrypt_decrypt_cycle(self):
        """Test that encryption followed by decryption recovers the original image."""
        # Encrypt
        encryptor = ImageEncryptor(quantum_seed=42)
        xor_key, permutation_key = encryptor.encrypt_image(
            self.test_image_path,
            self.encrypted_path,
            self.key_path
        )
        
        # Verify encrypted file exists
        self.assertTrue(os.path.exists(self.encrypted_path))
        self.assertTrue(os.path.exists(self.key_path))
        
        # Decrypt
        decryptor = ImageDecryptor()
        decryptor.decrypt_image(
            self.encrypted_path,
            self.decrypted_path,
            key_path=self.key_path
        )
        
        # Verify decrypted file exists
        self.assertTrue(os.path.exists(self.decrypted_path))
        
        # Compare original and decrypted images
        original = np.array(Image.open(self.test_image_path))
        decrypted = np.array(Image.open(self.decrypted_path))
        
        np.testing.assert_array_equal(original, decrypted)
    
    def test_encrypted_image_different_from_original(self):
        """Test that encrypted image is different from original."""
        encryptor = ImageEncryptor(quantum_seed=42)
        encryptor.encrypt_image(
            self.test_image_path,
            self.encrypted_path,
            self.key_path
        )
        
        original = np.array(Image.open(self.test_image_path))
        encrypted = np.array(Image.open(self.encrypted_path))
        
        # Images should be different
        self.assertFalse(np.array_equal(original, encrypted))
    
    def test_xor_encryption(self):
        """Test XOR encryption operation."""
        encryptor = ImageEncryptor(quantum_seed=42)
        
        data = np.array([1, 2, 3, 4, 5], dtype=np.uint8)
        key = bytes([255, 255, 255, 255, 255])
        
        encrypted = encryptor._xor_encrypt(data, key)
        decrypted = encryptor._xor_encrypt(encrypted, key)
        
        # XOR with same key twice should give original
        np.testing.assert_array_equal(data, decrypted)
    
    def test_pixel_permutation(self):
        """Test pixel permutation operation."""
        encryptor = ImageEncryptor(quantum_seed=42)
        
        data = np.array([1, 2, 3, 4, 5])
        permutation = np.array([4, 2, 0, 3, 1])
        
        permuted = encryptor._permute_pixels(data, permutation)
        
        # Check that permutation worked
        expected = np.array([5, 3, 1, 4, 2])
        np.testing.assert_array_equal(permuted, expected)
    
    def test_unpermute_pixels(self):
        """Test pixel unpermutation operation."""
        decryptor = ImageDecryptor()
        
        original = np.array([1, 2, 3, 4, 5])
        permutation = np.array([4, 2, 0, 3, 1])
        
        # Permute
        permuted = original[permutation]
        
        # Unpermute
        unpermuted = decryptor._unpermute_pixels(permuted, permutation)
        
        np.testing.assert_array_equal(original, unpermuted)
    
    def test_grayscale_image(self):
        """Test encryption/decryption with grayscale image."""
        # Create grayscale image
        gray_path = os.path.join(self.temp_dir, 'gray.png')
        img_array = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
        img = Image.fromarray(img_array, 'L')
        img.save(gray_path)
        
        # Encrypt and decrypt
        encryptor = ImageEncryptor(quantum_seed=42)
        encryptor.encrypt_image(gray_path, self.encrypted_path, self.key_path)
        
        decryptor = ImageDecryptor()
        decryptor.decrypt_image(self.encrypted_path, self.decrypted_path, key_path=self.key_path)
        
        # Compare
        original = np.array(Image.open(gray_path))
        decrypted = np.array(Image.open(self.decrypted_path))
        
        np.testing.assert_array_equal(original, decrypted)
    
    def test_different_image_sizes(self):
        """Test encryption/decryption with different image sizes."""
        sizes = [(32, 32, 3), (64, 128, 3), (100, 100, 3)]
        
        for size in sizes:
            with self.subTest(size=size):
                # Create test image
                img_path = os.path.join(self.temp_dir, f'test_{size[0]}x{size[1]}.png')
                img_array = np.random.randint(0, 256, size, dtype=np.uint8)
                img = Image.fromarray(img_array, 'RGB')
                img.save(img_path)
                
                # Encrypt and decrypt
                encryptor = ImageEncryptor(quantum_seed=42)
                encryptor.encrypt_image(img_path, self.encrypted_path, self.key_path)
                
                decryptor = ImageDecryptor()
                decryptor.decrypt_image(self.encrypted_path, self.decrypted_path, key_path=self.key_path)
                
                # Compare
                original = np.array(Image.open(img_path))
                decrypted = np.array(Image.open(self.decrypted_path))
                
                np.testing.assert_array_equal(original, decrypted)


if __name__ == '__main__':
    unittest.main()
