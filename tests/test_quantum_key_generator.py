"""
Tests for Quantum Key Generator module
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path to import from root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quantum_key_generator import QuantumKeyGenerator, generate_quantum_key


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
    
    def test_generate_keystream(self):
        """Test keystream generation."""
        keystream = self.qkg.generate_keystream(16)
        
        # Check length
        self.assertEqual(len(keystream), 16)
        
        # Check type
        self.assertIsInstance(keystream, np.ndarray)
    
    def test_generate_keystream_different_lengths(self):
        """Test keystream generation with different lengths."""
        for length in [1, 10, 100, 1000]:
            keystream = self.qkg.generate_keystream(length)
            self.assertEqual(len(keystream), length)
    
    def test_generate_permutation_seed(self):
        """Test permutation seed generation."""
        seed = self.qkg.generate_permutation_seed()
        
        # Check type
        self.assertIsInstance(seed, (int, np.integer))
        
        # Check that it's a valid seed value
        self.assertGreaterEqual(seed, 0)
    
    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results."""
        qkg1 = QuantumKeyGenerator(seed=123)
        qkg2 = QuantumKeyGenerator(seed=123)
        
        keystream1 = qkg1.generate_keystream(16)
        keystream2 = qkg2.generate_keystream(16)
        
        np.testing.assert_array_equal(keystream1, keystream2)
    
    def test_different_seeds_produce_different_results(self):
        """Test that different seeds produce different results."""
        qkg1 = QuantumKeyGenerator(seed=123)
        qkg2 = QuantumKeyGenerator(seed=456)
        
        keystream1 = qkg1.generate_keystream(16)
        keystream2 = qkg2.generate_keystream(16)
        
        # Arrays should be different
        self.assertFalse(np.array_equal(keystream1, keystream2))


if __name__ == '__main__':
    unittest.main()
