"""
Tests for Image Encryption and Decryption modules
"""

import unittest
import numpy as np
from PIL import Image
import os
import tempfile
import sys

# Add parent directory to path to import from root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from image_encryptor import ImageEncryptor, load_image_as_grayscale, save_image_array
from quantum_key_generator import generate_quantum_key


class TestEncryptionDecryption(unittest.TestCase):
    """Test cases for ImageEncryptor class."""
    
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
        # Load original image
        original_array = load_image_as_grayscale(self.test_image_path)
        
        # Generate quantum keys
        keystream, permutation_seed = generate_quantum_key(original_array.size, seed=42)
        
        # Encrypt
        encryptor = ImageEncryptor(keystream, permutation_seed)
        encrypted_array = encryptor.encrypt_image(original_array)
        
        # Save encrypted image
        save_image_array(encrypted_array, self.encrypted_path)
        self.assertTrue(os.path.exists(self.encrypted_path))
        
        # Decrypt
        decrypted_array = encryptor.decrypt_image(encrypted_array)
        
        # Save decrypted image
        save_image_array(decrypted_array, self.decrypted_path)
        self.assertTrue(os.path.exists(self.decrypted_path))
        
        # Compare original and decrypted images
        np.testing.assert_array_equal(original_array, decrypted_array)
    
    def test_encrypted_image_different_from_original(self):
        """Test that encrypted image is different from original."""
        # Load original image
        original_array = load_image_as_grayscale(self.test_image_path)
        
        # Generate quantum keys and encrypt
        keystream, permutation_seed = generate_quantum_key(original_array.size, seed=42)
        encryptor = ImageEncryptor(keystream, permutation_seed)
        encrypted_array = encryptor.encrypt_image(original_array)
        
        # Images should be different
        self.assertFalse(np.array_equal(original_array, encrypted_array))
    
    def test_xor_encryption(self):
        """Test XOR encryption operation."""
        data = np.array([1, 2, 3, 4, 5], dtype=np.uint8)
        key = np.array([255, 255, 255, 255, 255], dtype=np.uint8)
        
        # XOR encryption
        encrypted = np.bitwise_xor(data, key)
        # XOR decryption (XOR is self-inverse)
        decrypted = np.bitwise_xor(encrypted, key)
        
        # XOR with same key twice should give original
        np.testing.assert_array_equal(data, decrypted)
    
    def test_pixel_permutation(self):
        """Test pixel permutation operation."""
        data = np.array([1, 2, 3, 4, 5])
        permutation = np.array([4, 2, 0, 3, 1])
        
        # Apply permutation
        permuted = data[permutation]
        
        # Check that permutation worked
        expected = np.array([5, 3, 1, 4, 2])
        np.testing.assert_array_equal(permuted, expected)
    
    def test_unpermute_pixels(self):
        """Test pixel unpermutation operation."""
        original = np.array([1, 2, 3, 4, 5])
        permutation = np.array([4, 2, 0, 3, 1])
        
        # Permute
        permuted = original[permutation]
        
        # Unpermute using inverse permutation
        inverse_permutation = np.argsort(permutation)
        unpermuted = permuted[inverse_permutation]
        
        np.testing.assert_array_equal(original, unpermuted)
    
    def test_grayscale_image(self):
        """Test encryption/decryption with grayscale image."""
        # Create grayscale image
        gray_path = os.path.join(self.temp_dir, 'gray.png')
        img_array = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
        img = Image.fromarray(img_array, 'L')
        img.save(gray_path)
        
        # Load and process
        original_array = load_image_as_grayscale(gray_path)
        
        # Generate quantum keys and encrypt
        keystream, permutation_seed = generate_quantum_key(original_array.size, seed=42)
        encryptor = ImageEncryptor(keystream, permutation_seed)
        encrypted_array = encryptor.encrypt_image(original_array)
        
        # Decrypt
        decrypted_array = encryptor.decrypt_image(encrypted_array)
        
        # Compare
        np.testing.assert_array_equal(original_array, decrypted_array)
    
    def test_different_image_sizes(self):
        """Test encryption/decryption with different image sizes (grayscale only)."""
        sizes = [(32, 32), (64, 128), (100, 100)]
        
        for size in sizes:
            with self.subTest(size=size):
                # Create test grayscale image
                img_path = os.path.join(self.temp_dir, f'test_{size[0]}x{size[1]}.png')
                img_array = np.random.randint(0, 256, size, dtype=np.uint8)
                img = Image.fromarray(img_array, 'L')
                img.save(img_path)
                
                # Load and process
                original_array = load_image_as_grayscale(img_path)
                
                # Generate quantum keys and encrypt
                keystream, permutation_seed = generate_quantum_key(original_array.size, seed=42)
                encryptor = ImageEncryptor(keystream, permutation_seed)
                encrypted_array = encryptor.encrypt_image(original_array)
                
                # Decrypt
                decrypted_array = encryptor.decrypt_image(encrypted_array)
                
                # Compare
                np.testing.assert_array_equal(original_array, decrypted_array)


if __name__ == '__main__':
    unittest.main()
