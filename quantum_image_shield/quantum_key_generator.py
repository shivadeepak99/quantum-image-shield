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
    
    def generate_permutation_key(self, size: int) -> np.ndarray:
        """
        Generate a quantum random permutation for pixel shuffling.
        
        Args:
            size: Size of the permutation (number of elements)
            
        Returns:
            Random permutation array
        """
        # Generate enough random bits for shuffling
        # We need log2(size!) bits, but we'll use a simpler approach
        # Generate random bytes and use them to seed numpy's shuffle
        num_bytes = max(size // 2, 16)
        random_bytes = self.generate_key(num_bytes)
        
        # Use quantum random bytes to seed numpy for permutation
        rng = np.random.RandomState(int.from_bytes(random_bytes[:4], 'big'))
        permutation = np.arange(size)
        rng.shuffle(permutation)
        
        return permutation
