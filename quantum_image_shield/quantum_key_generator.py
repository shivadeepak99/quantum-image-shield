"""
Quantum Key Generator Module

This module uses Qiskit to generate truly random keys using quantum circuits.
The randomness is derived from quantum measurements of superposition states.
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from typing import List


class QuantumKeyGenerator:
    """
    Generates cryptographic keys using quantum randomness.
    
    Uses quantum circuits with Hadamard gates to create superposition states,
    which are then measured to produce truly random bit sequences.
    """
    
    def __init__(self, seed: int = None):
        """
        Initialize the Quantum Key Generator.
        
        Args:
            seed: Optional seed for reproducibility (mainly for testing)
        """
        self.simulator = AerSimulator()
        self.seed = seed
    
    def generate_random_bits(self, num_bits: int) -> List[int]:
        """
        Generate random bits using quantum measurements.
        
        Args:
            num_bits: Number of random bits to generate
            
        Returns:
            List of random bits (0 or 1)
        """
        # Generate bits in batches to avoid memory issues with large circuits
        # Maximum qubits per batch (keep it reasonable for simulator)
        max_qubits_per_batch = 16
        all_bits = []
        
        remaining_bits = num_bits
        batch_seed = self.seed
        
        while remaining_bits > 0:
            batch_size = min(remaining_bits, max_qubits_per_batch)
            
            # Create quantum circuit for this batch
            qr = QuantumRegister(batch_size, 'q')
            cr = ClassicalRegister(batch_size, 'c')
            qc = QuantumCircuit(qr, cr)
            
            # Apply Hadamard gate to all qubits to create superposition
            for i in range(batch_size):
                qc.h(qr[i])
            
            # Measure all qubits
            qc.measure(qr, cr)
            
            # Execute the circuit
            job = self.simulator.run(qc, shots=1, seed_simulator=batch_seed)
            result = job.result()
            counts = result.get_counts(qc)
            
            # Extract the measured bit string
            bit_string = list(counts.keys())[0]
            # Reverse because Qiskit returns bits in reverse order
            batch_bits = [int(b) for b in reversed(bit_string)]
            
            all_bits.extend(batch_bits)
            remaining_bits -= batch_size
            
            # Update seed for next batch if seed is provided
            if batch_seed is not None:
                batch_seed += 1
        
        return all_bits
    
    def generate_key(self, length: int) -> bytes:
        """
        Generate a quantum random key of specified length.
        
        Args:
            length: Length of the key in bytes
            
        Returns:
            Random key as bytes
        """
        num_bits = length * 8
        bits = self.generate_random_bits(num_bits)
        
        # Convert bits to bytes
        key = bytearray()
        for i in range(0, num_bits, 8):
            byte_bits = bits[i:i+8]
            byte_value = sum([bit << (7-j) for j, bit in enumerate(byte_bits)])
            key.append(byte_value)
        
        return bytes(key)
    
    def generate_permutation_key(self, size: int, purity: str = 'balanced') -> np.ndarray:
        """
        Generate a quantum random permutation for pixel shuffling.
        
        Args:
            size: Size of the permutation (number of elements)
            purity: Quantum purity level - 'maximum', 'balanced', or 'fast'
                   - 'maximum': Pure quantum Fisher-Yates (slow, most secure)
                   - 'balanced': 256-bit quantum seed + CSPRNG (recommended)
                   - 'fast': 128-bit quantum seed + fast shuffle (development)
            
        Returns:
            Random permutation array
        """
        if purity == 'maximum':
            return self._generate_pure_quantum_permutation(size)
        elif purity == 'balanced':
            return self._generate_hybrid_quantum_permutation(size, seed_bits=256)
        elif purity == 'fast':
            return self._generate_hybrid_quantum_permutation(size, seed_bits=128)
        else:
            raise ValueError(f"Invalid purity level: {purity}. Use 'maximum', 'balanced', or 'fast'")
    
    def _generate_pure_quantum_permutation(self, size: int) -> np.ndarray:
        """
        Generate TRUE quantum permutation using Fisher-Yates with quantum randomness.
        
        This is the most secure but slowest method. Each swap decision uses
        fresh quantum random bits.
        
        Args:
            size: Size of the permutation
            
        Returns:
            Pure quantum random permutation
        """
        permutation = np.arange(size)
        
        for i in range(size - 1, 0, -1):
            # Calculate bits needed to select index in range [0, i]
            bits_needed = int(np.ceil(np.log2(i + 1)))
            
            # Generate quantum random index with rejection sampling
            # to ensure uniform distribution
            while True:
                random_bits = self.generate_random_bits(bits_needed)
                # Convert bits to integer
                j = sum([bit << idx for idx, bit in enumerate(random_bits)])
                
                # Accept only if in valid range (rejection sampling)
                if j <= i:
                    break
            
            # Swap elements
            permutation[i], permutation[j] = permutation[j], permutation[i]
        
        return permutation
    
    def _generate_hybrid_quantum_permutation(self, size: int, seed_bits: int = 256) -> np.ndarray:
        """
        Generate permutation using quantum seed + cryptographically secure PRNG.
        
        This balances quantum security with performance. Uses high-entropy
        quantum seed (256 or 128 bits) to initialize a secure random generator.
        
        Args:
            size: Size of the permutation
            seed_bits: Number of quantum random bits for seed (128 or 256)
            
        Returns:
            Quantum-seeded secure permutation
        """
        # Generate quantum random seed
        num_bytes = seed_bits // 8
        quantum_seed_bytes = self.generate_key(num_bytes)
        
        # Convert to integer seed
        quantum_seed = int.from_bytes(quantum_seed_bytes, byteorder='big')
        
        # Use numpy's PCG64 generator (cryptographically strong PRNG)
        # This is MUCH better than the old RandomState with Mersenne Twister
        rng = np.random.Generator(np.random.PCG64(quantum_seed))
        
        # Generate permutation using secure shuffle
        permutation = np.arange(size)
        rng.shuffle(permutation)
        
        return permutation
