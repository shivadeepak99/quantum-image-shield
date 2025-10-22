"""
Unit tests for Quantum Key Generator

Tests quantum randomness, permutation generation, and statistical properties.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from quantum_image_shield.quantum_key_generator import QuantumKeyGenerator


class TestQuantumKeyGenerator:
    """Test suite for QuantumKeyGenerator class."""
    
    def test_initialization(self):
        """Test generator initialization."""
        gen = QuantumKeyGenerator()
        assert gen.simulator is not None
        assert gen.seed is None
        
        gen_with_seed = QuantumKeyGenerator(seed=42)
        assert gen_with_seed.seed == 42
    
    def test_generate_random_bits_length(self):
        """Test that generated bits have correct length."""
        gen = QuantumKeyGenerator(seed=42)
        
        for num_bits in [8, 16, 32, 100, 1000]:
            bits = gen.generate_random_bits(num_bits)
            assert len(bits) == num_bits, f"Expected {num_bits} bits, got {len(bits)}"
    
    def test_generate_random_bits_binary(self):
        """Test that generated bits are only 0 or 1."""
        gen = QuantumKeyGenerator(seed=42)
        bits = gen.generate_random_bits(1000)
        
        assert all(bit in [0, 1] for bit in bits), "Bits must be 0 or 1"
    
    def test_generate_random_bits_distribution(self):
        """Test that bits have approximately 50/50 distribution."""
        gen = QuantumKeyGenerator(seed=42)
        bits = gen.generate_random_bits(10000)
        
        ones = sum(bits)
        zeros = len(bits) - ones
        
        # Should be roughly 50/50 (within 5% tolerance)
        assert 4500 <= ones <= 5500, f"Distribution skewed: {ones} ones, {zeros} zeros"
        assert 4500 <= zeros <= 5500
    
    def test_generate_key_length(self):
        """Test that generated keys have correct length."""
        gen = QuantumKeyGenerator(seed=42)
        
        for length in [1, 10, 100, 1000]:
            key = gen.generate_key(length)
            assert len(key) == length, f"Expected {length} bytes, got {len(key)}"
            assert isinstance(key, bytes)
    
    def test_permutation_balanced_is_permutation(self):
        """Test that balanced permutation contains all indices exactly once."""
        gen = QuantumKeyGenerator(seed=42)
        size = 1000
        
        perm = gen.generate_permutation_key(size, purity='balanced')
        
        # Should contain all numbers from 0 to size-1
        assert set(perm) == set(range(size))
        
        # Should have no duplicates
        assert len(set(perm)) == size
    
    def test_permutation_all_purities_valid(self):
        """Test all purity levels produce valid permutations."""
        gen = QuantumKeyGenerator(seed=42)
        size = 100
        
        for purity in ['maximum', 'balanced', 'fast']:
            perm = gen.generate_permutation_key(size, purity=purity)
            
            assert len(perm) == size
            assert set(perm) == set(range(size))
    
    def test_permutation_invalid_purity_raises(self):
        """Test that invalid purity level raises error."""
        gen = QuantumKeyGenerator(seed=42)
        
        with pytest.raises(ValueError, match="Invalid purity level"):
            gen.generate_permutation_key(100, purity='invalid')
    
    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results."""
        seed = 12345
        
        gen1 = QuantumKeyGenerator(seed=seed)
        gen2 = QuantumKeyGenerator(seed=seed)
        
        # Generate keys
        key1 = gen1.generate_key(100)
        key2 = gen2.generate_key(100)
        
        assert key1 == key2, "Same seed should produce same key"
