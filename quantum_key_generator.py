"""
Quantum Key Generator Module

This module generates cryptographic keys using quantum circuits.
It leverages Qiskit to simulate quantum randomness through Hadamard gates
and measurements, producing truly random bit sequences for encryption.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


class QuantumKeyGenerator:
    """
    Generates cryptographic keys using quantum circuits.
    
    Uses Hadamard gates to create superposition states and measurements
    to collapse them into random bit sequences.
    """
    
    def __init__(self, seed=None):
        """
        Initialize the quantum key generator.
        
        Args:
            seed: Optional seed for reproducibility in testing
        """
        self.simulator = AerSimulator()
        self.seed = seed
    
    def generate_random_bits(self, num_bits):
        """
        Generate random bits using quantum circuits.
        
        Args:
            num_bits: Number of random bits to generate
            
        Returns:
            numpy array of random bits (0s and 1s)
        """
        # Create quantum circuit with required number of qubits
        # Use multiple shots to generate more bits efficiently
        max_qubits_per_circuit = 20
        shots_per_circuit = 100  # Generate multiple measurements per circuit
        bits = []
        
        remaining_bits = num_bits
        while remaining_bits > 0:
            qubits_needed = min(remaining_bits, max_qubits_per_circuit)
            shots_needed = min(shots_per_circuit, (remaining_bits + qubits_needed - 1) // qubits_needed)
            
            # Create circuit
            qc = QuantumCircuit(qubits_needed, qubits_needed)
            
            # Apply Hadamard gate to each qubit to create superposition
            for i in range(qubits_needed):
                qc.h(i)
            
            # Measure all qubits
            qc.measure(range(qubits_needed), range(qubits_needed))
            
            # Transpile and run with multiple shots
            transpiled_qc = transpile(qc, self.simulator)
            job = self.simulator.run(transpiled_qc, shots=shots_needed, seed_simulator=self.seed)
            result = job.result()
            counts = result.get_counts()
            
            # Extract bits from all measurements
            for measurement in counts.keys():
                if remaining_bits <= 0:
                    break
                # Convert to array of bits (reverse to match qubit ordering)
                circuit_bits = [int(b) for b in reversed(measurement)]
                bits.extend(circuit_bits[:remaining_bits])
                remaining_bits -= len(circuit_bits[:remaining_bits])
        
        return np.array(bits[:num_bits], dtype=np.uint8)
    
    def generate_keystream(self, length):
        """
        Generate a keystream of specified length.
        
        Args:
            length: Length of keystream in bytes
            
        Returns:
            numpy array of random bytes (0-255)
        """
        # Generate 8 bits for each byte needed
        num_bits = length * 8
        bits = self.generate_random_bits(num_bits)
        
        # Convert bits to bytes
        keystream = np.zeros(length, dtype=np.uint8)
        for i in range(length):
            byte_bits = bits[i*8:(i+1)*8]
            keystream[i] = int(''.join(map(str, byte_bits)), 2)
        
        return keystream
    
    def generate_permutation_seed(self):
        """
        Generate a seed for permutation operations.
        
        Returns:
            Integer seed derived from quantum randomness
        """
        # Generate 32 bits for a seed
        bits = self.generate_random_bits(32)
        seed_value = int(''.join(map(str, bits)), 2)
        return seed_value


def generate_quantum_key(image_size, seed=None):
    """
    Convenience function to generate quantum key for an image.
    
    Args:
        image_size: Total number of pixels in the image
        seed: Optional seed for reproducibility
        
    Returns:
        tuple: (keystream, permutation_seed)
    """
    generator = QuantumKeyGenerator(seed=seed)
    keystream = generator.generate_keystream(image_size)
    permutation_seed = generator.generate_permutation_seed()
    return keystream, permutation_seed
