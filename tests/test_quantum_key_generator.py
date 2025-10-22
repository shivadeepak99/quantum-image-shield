"""Unit tests for quantum key generator"""

import unittest
import numpy as np
from quantum_image_shield.quantum_key_generator import QuantumKeyGenerator


class TestQuantumKeyGenerator(unittest.TestCase):
    """Test cases for QuantumKeyGenerator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = QuantumKeyGenerator()
    
    def test_generate_random_bits(self):
        """Test random bit generation"""
        num_bits = 100
        bits = self.generator.generate_random_bits(num_bits)
        
        # Check correct length
        self.assertEqual(len(bits), num_bits)
        
        # Check all bits are 0 or 1
        self.assertTrue(all(bit in [0, 1] for bit in bits))
    
    def test_generate_key(self):
        """Test encryption key generation"""
        length = 100
        key = self.generator.generate_key(length)
        
        # Check correct length
        self.assertEqual(len(key), length)
        
        # Check correct type
        self.assertIsInstance(key, bytes)
        
        # Check values in valid range
        self.assertTrue(all(0 <= byte <= 255 for byte in key))
    
    def test_generate_permutation_key(self):
        """Test permutation key generation"""
        size = 100
        perm_key = self.generator.generate_permutation_key(size)
        
        # Check correct length
        self.assertEqual(len(perm_key), size)
        
        # Check all indices are unique
        self.assertEqual(len(set(perm_key)), size)
        
        # Check values in valid range
        self.assertTrue(all(0 <= idx < size for idx in perm_key))
    
    def test_randomness_quality(self):
        """Test that generated bits have good randomness"""
        num_bits = 10000
        bits = self.generator.generate_random_bits(num_bits)
        
        # Check distribution (should be roughly 50/50)
        ones_ratio = sum(bits) / len(bits)
        self.assertTrue(0.45 < ones_ratio < 0.55, 
                       f"Bit distribution too skewed: {ones_ratio}")
    
    def test_key_uniqueness(self):
        """Test that generated keys are unique"""
        length = 100
        key1 = self.generator.generate_key(length)
        key2 = self.generator.generate_key(length)
        
        # Keys should be different
        self.assertNotEqual(key1, key2)
    
    def test_permutation_is_valid(self):
        """Test that permutation is a valid shuffle"""
        size = 100
        perm_key = self.generator.generate_permutation_key(size)
        
        # Should contain all indices from 0 to size-1
        self.assertEqual(sorted(perm_key), list(range(size)))


if __name__ == '__main__':
    unittest.main()
