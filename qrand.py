# qrand.py
"""Quantum random bit generator with Qiskit.
Provides:
- quantum_random_bits(n_bits): returns `n_bits` random bits as a numpy uint8 array of 0/1.
- random_bytes_from_quantum(n_bytes): returns n_bytes as numpy uint8 array (0..255).

Fallback: if Qiskit Aer backend not available, falls back to numpy's RNG (only for development/testing).
"""

from typing import Tuple
import numpy as np

try:
    from qiskit import QuantumCircuit, Aer, execute
    AER_AVAILABLE = True
except Exception:
    AER_AVAILABLE = False

def quantum_random_bits(n_bits: int) -> np.ndarray:
    """Return n_bits random bits (0/1) using Qiskit Aer simulator.

    If Aer is not available, uses numpy's RNG as a fallback (not quantum).
    """
    if n_bits <= 0:
        return np.array([], dtype=np.uint8)

    if AER_AVAILABLE:
        # If the number of bits is large, construct multiple smaller circuits to avoid exceeding backend limits.
        bits = []
        max_qubits = 24  # tuneable: keep circuits small to avoid simulator limits
        remaining = n_bits
        while remaining > 0:
            k = min(max_qubits, remaining)
            qc = QuantumCircuit(k, k)
            qc.h(range(k))
            qc.measure_all()
            backend = Aer.get_backend('qasm_simulator')
            job = execute(qc, backend=backend, shots=1)
            result = job.result()
            counts = list(result.get_counts().keys())[0]
            # counts is e.g. '0101' (big-endian string) — reverse to little-endian order
            bits_chunk = [int(b) for b in counts[::-1]]
            bits.extend(bits_chunk)
            remaining -= k
        return np.array(bits[:n_bits], dtype=np.uint8)
    else:
        # Fallback for development: use numpy RNG
        rng = np.random.default_rng()
        return rng.integers(0, 2, size=n_bits, dtype=np.uint8)

def random_bytes_from_quantum(n_bytes: int) -> np.ndarray:
    """Return n_bytes of random values 0..255 as numpy uint8, generated from quantum bits.

    Packs bits into bytes (MSB order inside each byte).
    """
    n_bits = n_bytes * 8
    bits = quantum_random_bits(n_bits)
    bits = bits.reshape(n_bytes, 8)
    # pack each 8-bit row into a byte (msb first)
    bytes_out = np.zeros(n_bytes, dtype=np.uint8)
    for i in range(n_bytes):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | int(bits[i, j])
        bytes_out[i] = byte
    return bytes_out
