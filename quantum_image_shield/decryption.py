"""
Image Decryption Module

Implements decryption operations to reverse the encryption process.
"""

import numpy as np
from PIL import Image
from typing import Tuple


class ImageDecryptor:
    """
    Decrypts images that were encrypted using the ImageEncryptor.
    
    The decryption process reverses:
    1. Pixel permutation (unshuffling)
    2. XOR operation with the same key
    """
    
    def decrypt_image(self, encrypted_path: str, output_path: str, 
                     xor_key: bytes = None, permutation_key: np.ndarray = None,
                     key_path: str = None, original_shape: Tuple = None,
                     original_mode: str = None) -> np.ndarray:
        """
        Decrypt an encrypted image file.
        
        Args:
            encrypted_path: Path to the encrypted image
            output_path: Path to save the decrypted image
            xor_key: XOR key (if not loading from key_path)
            permutation_key: Permutation key (if not loading from key_path)
            key_path: Path to load keys from
            original_shape: Original image shape (if not loading from key_path)
            original_mode: Original image mode (if not loading from key_path)
            
        Returns:
            Decrypted image array
        """
        # Load keys if key_path provided
        if key_path:
            xor_key, permutation_key, original_shape, original_mode = self._load_keys(key_path)
        
        if xor_key is None or permutation_key is None:
            raise ValueError("Either provide keys directly or specify key_path")
        
        # Load the encrypted image
        encrypted_img = Image.open(encrypted_path)
        encrypted_array = np.array(encrypted_img)
        
        # Flatten the array
        flat_encrypted = encrypted_array.flatten()
        
        # Step 1: Reverse the permutation (unshuffle)
        unpermuted = self._unpermute_pixels(flat_encrypted, permutation_key)
        
        # Step 2: Apply XOR decryption (XOR is self-inverse)
        decrypted = self._xor_decrypt(unpermuted, xor_key)
        
        # Reshape to original shape
        if original_shape is None:
            original_shape = encrypted_array.shape
        if original_mode is None:
            original_mode = encrypted_img.mode
            
        decrypted_array = decrypted.reshape(original_shape)
        
        # Save decrypted image
        decrypted_img = Image.fromarray(decrypted_array.astype(np.uint8), mode=original_mode)
        decrypted_img.save(output_path)
        
        return decrypted_array
    
    def _unpermute_pixels(self, data: np.ndarray, permutation: np.ndarray) -> np.ndarray:
        """
        Reverse the pixel permutation.
        
        Args:
            data: Permuted data array
            permutation: Original permutation indices
            
        Returns:
            Unpermuted data
        """
        # Create inverse permutation
        inverse_permutation = np.argsort(permutation)
        return data[inverse_permutation]
    
    def _xor_decrypt(self, data: np.ndarray, key: bytes) -> np.ndarray:
        """
        Apply XOR decryption (same as encryption since XOR is self-inverse).
        
        Args:
            data: Encrypted data array
            key: XOR key bytes
            
        Returns:
            Decrypted data
        """
        key_array = np.frombuffer(key, dtype=np.uint8)
        return np.bitwise_xor(data, key_array)
    
    def _load_keys(self, key_path: str) -> Tuple[bytes, np.ndarray, Tuple, str]:
        """
        Load encryption keys from file.
        
        Args:
            key_path: Path to key file
            
        Returns:
            Tuple of (xor_key, permutation_key, shape, mode)
        """
        keys = np.load(key_path, allow_pickle=True)
        xor_key = keys['xor_key'].tobytes()
        permutation_key = keys['permutation_key']
        shape = tuple(keys['shape'])
        mode = str(keys['mode'])
        return xor_key, permutation_key, shape, mode
