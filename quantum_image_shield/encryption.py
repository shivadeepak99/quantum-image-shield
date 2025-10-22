"""
Image Encryption Module

Implements classical encryption operations including XOR cipher and pixel permutation.
"""

import numpy as np
from PIL import Image
from typing import Tuple
from .quantum_key_generator import QuantumKeyGenerator


class ImageEncryptor:
    """
    Encrypts images using quantum-generated keys and classical encryption techniques.
    
    The encryption process involves:
    1. XOR operation with quantum-generated key
    2. Pixel permutation (shuffling) based on quantum randomness
    
    Supports both file-based and array-based workflows.
    """
    
    def __init__(self, quantum_seed: int = None, quantum_purity: str = 'balanced'):
        """
        Initialize the Image Encryptor.
        
        Args:
            quantum_seed: Optional seed for quantum key generation (testing only)
            quantum_purity: Quantum purity level - 'maximum', 'balanced', or 'fast'
                           Default: 'balanced' (recommended for production)
        """
        self.key_generator = QuantumKeyGenerator(seed=quantum_seed)
        self.quantum_purity = quantum_purity
        self.last_xor_key = None
        self.last_permutation_key = None
    
    def encrypt_image(self, image_path: str, output_path: str, key_path: str = None) -> Tuple[bytes, np.ndarray]:
        """
        Encrypt an image file.
        
        Args:
            image_path: Path to the input image
            output_path: Path to save the encrypted image
            key_path: Optional path to save the encryption keys
            
        Returns:
            Tuple of (xor_key, permutation_key)
        """
        # Load the image
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Store original shape and mode
        original_shape = img_array.shape
        original_mode = img.mode
        
        # Flatten the image array
        flat_img = img_array.flatten()
        
        # Step 1: Generate quantum random XOR key
        xor_key = self.key_generator.generate_key(len(flat_img))
        
        # Step 2: Apply XOR encryption
        xor_encrypted = self._xor_encrypt(flat_img, xor_key)
        
        # Step 3: Generate quantum random permutation
        permutation_key = self.key_generator.generate_permutation_key(
            len(xor_encrypted), 
            purity=self.quantum_purity
        )
        
        # Step 4: Apply pixel permutation
        permuted = self._permute_pixels(xor_encrypted, permutation_key)
        
        # Reshape back to original shape
        encrypted_array = permuted.reshape(original_shape)
        
        # Save encrypted image
        encrypted_img = Image.fromarray(encrypted_array.astype(np.uint8), mode=original_mode)
        encrypted_img.save(output_path)
        
        # Save keys if path provided
        if key_path:
            self._save_keys(key_path, xor_key, permutation_key, original_shape, original_mode)
        
        return xor_key, permutation_key
    
    def encrypt_array(self, image_array: np.ndarray) -> np.ndarray:
        """
        Encrypt a numpy array directly (for in-memory processing).
        
        This method is useful for Streamlit apps, batch processing,
        or when you want to work with arrays instead of files.
        
        Args:
            image_array: Numpy array representing the image
            
        Returns:
            Encrypted numpy array with same shape as input
            
        Note:
            Keys are stored in self.last_xor_key and self.last_permutation_key
            for later decryption.
        """
        # Store original shape
        original_shape = image_array.shape
        flat_img = image_array.flatten()
        
        # Generate quantum random XOR key
        xor_key = self.key_generator.generate_key(len(flat_img))
        
        # Apply XOR encryption
        xor_encrypted = self._xor_encrypt(flat_img, xor_key)
        
        # Generate quantum random permutation
        permutation_key = self.key_generator.generate_permutation_key(
            len(xor_encrypted),
            purity=self.quantum_purity
        )
        
        # Apply pixel permutation
        permuted = self._permute_pixels(xor_encrypted, permutation_key)
        
        # Store keys for later decryption
        self.last_xor_key = xor_key
        self.last_permutation_key = permutation_key
        
        # Reshape back to original shape
        return permuted.reshape(original_shape)
    
    def get_last_keys(self) -> Tuple[bytes, np.ndarray]:
        """
        Get the keys from the last array encryption.
        
        Returns:
            Tuple of (xor_key, permutation_key)
        """
        if self.last_xor_key is None or self.last_permutation_key is None:
            raise ValueError("No encryption has been performed yet")
        return self.last_xor_key, self.last_permutation_key
    
    def _xor_encrypt(self, data: np.ndarray, key: bytes) -> np.ndarray:
        """
        Apply XOR encryption to data.
        
        Args:
            data: Input data array
            key: XOR key bytes
            
        Returns:
            XOR encrypted data
        """
        key_array = np.frombuffer(key, dtype=np.uint8)
        return np.bitwise_xor(data, key_array)
    
    def _permute_pixels(self, data: np.ndarray, permutation: np.ndarray) -> np.ndarray:
        """
        Permute pixels based on permutation key.
        
        Args:
            data: Input data array
            permutation: Permutation indices
            
        Returns:
            Permuted data
        """
        return data[permutation]
    
    def _save_keys(self, key_path: str, xor_key: bytes, permutation_key: np.ndarray, 
                   shape: Tuple, mode: str):
        """
        Save encryption keys to file.
        
        Args:
            key_path: Path to save keys
            xor_key: XOR encryption key
            permutation_key: Permutation indices
            shape: Original image shape
            mode: Original image mode
        """
        key_data = {
            'xor_key': xor_key,
            'permutation_key': permutation_key,
            'shape': shape,
            'mode': mode,
            'quantum_purity': self.quantum_purity,
            'version': '2.0'
        }
        np.savez_compressed(key_path, 
                          xor_key=np.frombuffer(xor_key, dtype=np.uint8),
                          permutation_key=permutation_key,
                          shape=np.array(shape),
                          mode=mode,
                          quantum_purity=self.quantum_purity,
                          version='2.0')
