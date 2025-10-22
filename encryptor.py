# encryptor.py
import numpy as np
from typing import Tuple
from qrand import random_bytes_from_quantum

class QuantumSeedImageShield:
    def __init__(self, img_shape: Tuple[int, int]):
        self.img_shape = img_shape
        self.N = img_shape[0] * img_shape[1]
        self.keystream = None  # numpy uint8 array length N
        self.permutation = None
        self.seed = None

    def generate_keystream_and_permutation(self):
        # Get N bytes from quantum RNG
        self.keystream = random_bytes_from_quantum(self.N)

        # For permutation seed, we ask for 32 bits from quantum RNG and convert to integer
        seed_bytes = random_bytes_from_quantum(4)
        seed = 0
        for b in seed_bytes:
            seed = (seed << 8) | int(b)
        self.seed = int(seed & 0xFFFFFFFF)

        # Use numpy RNG seeded by quantum-derived seed to create a permutation
        rng = np.random.default_rng(self.seed)
        self.permutation = rng.permutation(self.N)

    def encrypt(self, img: np.ndarray) -> np.ndarray:
        """Encrypt a 2D grayscale image. Returns encrypted 2D array."""
        flat = img.flatten().astype(np.uint8)
        if self.keystream is None or self.permutation is None:
            self.generate_keystream_and_permutation()
        xorred = np.bitwise_xor(flat, self.keystream[:self.N])
        permuted = xorred[self.permutation]
        return permuted.reshape(self.img_shape).astype(np.uint8)

    def decrypt(self, encrypted_img: np.ndarray) -> np.ndarray:
        """Decrypt with the existing keystream and permutation. Returns the reconstructed image."""
        if self.keystream is None or self.permutation is None:
            raise ValueError("Keystream and permutation not set. You must run encrypt (or set keys) first.")
        flat = encrypted_img.flatten().astype(np.uint8)
        # reverse permutation
        reverse_perm = np.argsort(self.permutation)
        unpermuted = flat[reverse_perm]
        recovered = np.bitwise_xor(unpermuted, self.keystream[:self.N])
        return recovered.reshape(self.img_shape).astype(np.uint8)

    def export_keys(self) -> dict:
        return {'keystream': self.keystream.copy(), 'permutation': self.permutation.copy(), 'seed': self.seed}

    def import_keys(self, keys: dict):
        self.keystream = keys['keystream'].copy()
        self.permutation = keys['permutation'].copy()
        self.seed = int(keys['seed'])
