"""Unit tests for image encryption and decryption"""

import unittest
import numpy as np
from PIL import Image
import tempfile
import os
from quantum_image_shield.encryption import ImageEncryptor
from quantum_image_shield.decryption import ImageDecryptor


class TestEncryptionDecryption(unittest.TestCase):
    """Test cases for image encryption and decryption"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.encryptor = ImageEncryptor()
        self.decryptor = ImageDecryptor()
        
        # Create a temporary test image
        self.test_image_array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        self.test_image = Image.fromarray(self.test_image_array)
        
        # Create temporary file paths
        self.temp_dir = tempfile.mkdtemp()
        self.test_image_path = os.path.join(self.temp_dir, 'test.png')
        self.encrypted_path = os.path.join(self.temp_dir, 'encrypted.png')
        self.decrypted_path = os.path.join(self.temp_dir, 'decrypted.png')
        self.key_path = os.path.join(self.temp_dir, 'keys.npz')
        
        # Save test image
        self.test_image.save(self.test_image_path)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_encrypt_array(self):
        """Test array-based encryption"""
        encrypted_array = self.encryptor.encrypt_array(self.test_image_array)
        
        # Encrypted image should have same shape
        self.assertEqual(encrypted_array.shape, self.test_image_array.shape)
        
        # Encrypted image should be different from original
        self.assertFalse(np.array_equal(encrypted_array, self.test_image_array))
    
    def test_decrypt_array(self):
        """Test array-based decryption"""
        # Encrypt
        encrypted_array = self.encryptor.encrypt_array(self.test_image_array)
        xor_key, permutation_key = self.encryptor.get_last_keys()
        
        # Decrypt
        decrypted_array = self.decryptor.decrypt_array(encrypted_array, xor_key, permutation_key)
        
        # Decrypted should match original
        np.testing.assert_array_equal(decrypted_array, self.test_image_array)
    
    def test_encrypt_image_file(self):
        """Test file-based encryption"""
        self.encryptor.encrypt_image(
            self.test_image_path,
            self.encrypted_path,
            self.key_path
        )
        
        # Check that files were created
        self.assertTrue(os.path.exists(self.encrypted_path))
        self.assertTrue(os.path.exists(self.key_path))
    
    def test_decrypt_image_file(self):
        """Test file-based decryption"""
        # Encrypt
        self.encryptor.encrypt_image(
            self.test_image_path,
            self.encrypted_path,
            self.key_path
        )
        
        # Decrypt
        self.decryptor.decrypt_image(
            self.encrypted_path,
            self.decrypted_path,
            key_path=self.key_path
        )
        
        # Load both images
        original = np.array(Image.open(self.test_image_path))
        decrypted = np.array(Image.open(self.decrypted_path))
        
        # Should be identical
        np.testing.assert_array_equal(decrypted, original)
    
    def test_encryption_randomness(self):
        """Test that encryption produces random-looking output"""
        encrypted = self.encryptor.encrypt_array(self.test_image_array)
        
        # Calculate correlation between adjacent pixels
        h_correlation = np.corrcoef(
            encrypted[:, :-1].flatten(),
            encrypted[:, 1:].flatten()
        )[0, 1]
        
        # Low correlation indicates good randomness
        self.assertLess(abs(h_correlation), 0.1,
                       f"Encryption has too high correlation: {h_correlation}")
    
    def test_grayscale_image(self):
        """Test encryption/decryption of grayscale image"""
        # Create grayscale test image
        gray_array = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        
        # Encrypt and decrypt
        encrypted = self.encryptor.encrypt_array(gray_array)
        xor_key, permutation_key = self.encryptor.get_last_keys()
        decrypted = self.decryptor.decrypt_array(encrypted, xor_key, permutation_key)
        
        # Should match original
        np.testing.assert_array_equal(decrypted, gray_array)


if __name__ == '__main__':
    unittest.main()
