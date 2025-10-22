"""
Image Encryption/Decryption Module

This module implements hybrid quantum-classical image encryption using
XOR operations with quantum-generated keystreams and pixel permutations.
"""

import numpy as np
from PIL import Image
import io


class ImageEncryptor:
    """
    Handles encryption and decryption of grayscale images using
    quantum-generated keys and classical encryption techniques.
    """
    
    def __init__(self, keystream, permutation_seed):
        """
        Initialize the encryptor with keys.
        
        Args:
            keystream: numpy array of random bytes for XOR operation
            permutation_seed: seed for pixel permutation
        """
        self.keystream = keystream
        self.permutation_seed = permutation_seed
    
    def encrypt_image(self, image_array):
        """
        Encrypt an image using XOR and permutation.
        
        Args:
            image_array: 2D numpy array of pixel values
            
        Returns:
            2D numpy array of encrypted pixel values
        """
        # Flatten image to 1D array
        original_shape = image_array.shape
        flat_image = image_array.flatten()
        
        # Step 1: XOR with quantum keystream
        encrypted = np.bitwise_xor(flat_image, self.keystream)
        
        # Step 2: Permute pixels
        np.random.seed(self.permutation_seed)
        permutation_indices = np.random.permutation(len(encrypted))
        encrypted_permuted = encrypted[permutation_indices]
        
        # Reshape back to original dimensions
        encrypted_image = encrypted_permuted.reshape(original_shape)
        
        return encrypted_image
    
    def decrypt_image(self, encrypted_array):
        """
        Decrypt an image by reversing the encryption process.
        
        Args:
            encrypted_array: 2D numpy array of encrypted pixel values
            
        Returns:
            2D numpy array of decrypted pixel values
        """
        # Flatten image to 1D array
        original_shape = encrypted_array.shape
        flat_encrypted = encrypted_array.flatten()
        
        # Step 1: Reverse permutation
        np.random.seed(self.permutation_seed)
        permutation_indices = np.random.permutation(len(flat_encrypted))
        
        # Create inverse permutation
        inverse_permutation = np.argsort(permutation_indices)
        depermuted = flat_encrypted[inverse_permutation]
        
        # Step 2: XOR with quantum keystream (XOR is self-inverse)
        decrypted = np.bitwise_xor(depermuted, self.keystream)
        
        # Reshape back to original dimensions
        decrypted_image = decrypted.reshape(original_shape)
        
        return decrypted_image


def load_image_as_grayscale(image_path_or_bytes):
    """
    Load an image and convert to grayscale numpy array.
    
    Args:
        image_path_or_bytes: File path string or bytes object
        
    Returns:
        numpy array of pixel values (0-255)
    """
    if isinstance(image_path_or_bytes, bytes):
        image = Image.open(io.BytesIO(image_path_or_bytes))
    else:
        image = Image.open(image_path_or_bytes)
    
    # Convert to grayscale
    grayscale = image.convert('L')
    
    # Convert to numpy array
    image_array = np.array(grayscale, dtype=np.uint8)
    
    return image_array


def save_image_array(image_array, output_path):
    """
    Save a numpy array as an image file.
    
    Args:
        image_array: 2D numpy array of pixel values
        output_path: Path to save the image
    """
    image = Image.fromarray(image_array.astype(np.uint8), mode='L')
    image.save(output_path)


def array_to_image_bytes(image_array):
    """
    Convert numpy array to image bytes (for Streamlit display).
    
    Args:
        image_array: 2D numpy array of pixel values
        
    Returns:
        bytes object containing PNG image data
    """
    image = Image.fromarray(image_array.astype(np.uint8), mode='L')
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    return buf.getvalue()
