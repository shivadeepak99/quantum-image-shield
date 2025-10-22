"""
Tests for Quantum Key Generator module
"""

import unittest
import numpy as np
from quantum_image_shield.quantum_key_generator import QuantumKeyGenerator


class TestQuantumKeyGenerator(unittest.TestCase):
    """Test cases for QuantumKeyGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.qkg = QuantumKeyGenerator(seed=42)
    
    def test_generate_random_bits(self):
        """Test random bit generation."""
        bits = self.qkg.generate_random_bits(16)
        
        # Check length
        self.assertEqual(len(bits), 16)
        
        # Check that all values are 0 or 1
        for bit in bits:
            self.assertIn(bit, [0, 1])
    
    def test_generate_random_bits_different_lengths(self):
        """Test random bit generation with different lengths."""
        for length in [8, 32, 64, 128]:
            bits = self.qkg.generate_random_bits(length)
            self.assertEqual(len(bits), length)
    
    def test_generate_key(self):
        """Test key generation."""
        key = self.qkg.generate_key(16)
        
        # Check length
        self.assertEqual(len(key), 16)
        
        # Check type
        self.assertIsInstance(key, bytes)
    
    def test_generate_key_different_lengths(self):
        """Test key generation with different lengths."""
        for length in [1, 10, 100, 1000]:
            key = self.qkg.generate_key(length)
            self.assertEqual(len(key), length)
    
    def test_generate_permutation_key(self):
        """Test permutation key generation."""
        size = 100
        permutation = self.qkg.generate_permutation_key(size)
        
        # Check length
        self.assertEqual(len(permutation), size)
        
        # Check that it's a valid permutation (contains all indices)
        self.assertEqual(set(permutation), set(range(size)))
    
    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results."""
        qkg1 = QuantumKeyGenerator(seed=123)
        qkg2 = QuantumKeyGenerator(seed=123)
        
        key1 = qkg1.generate_key(16)
        key2 = qkg2.generate_key(16)
        
        self.assertEqual(key1, key2)
    
    def test_different_seeds_produce_different_results(self):
        """Test that different seeds produce different results."""
        qkg1 = QuantumKeyGenerator(seed=123)
        qkg2 = QuantumKeyGenerator(seed=456)
        
        key1 = qkg1.generate_key(16)
        key2 = qkg2.generate_key(16)
        
        self.assertNotEqual(key1, key2)


if __name__ == '__main__':
    unittest.main()
