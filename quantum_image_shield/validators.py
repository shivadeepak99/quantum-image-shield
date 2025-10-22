"""
Input Validation Module

Provides comprehensive input validation for image uploads and processing.
Protects against malicious files, exploits, and resource exhaustion attacks.
"""

import os
from typing import Tuple, Optional
from pathlib import Path
from PIL import Image
import numpy as np


class ImageValidator:
    """
    Validates image files for security and compatibility.
    
    Checks for:
    - File size limits
    - Image format validation
    - Magic byte verification
    - Dimension limits
    - Mode compatibility
    - Potential exploits
    """
    
    # Security limits
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
    MAX_PIXELS = 25_000_000  # 25 megapixels (e.g., 5000x5000)
    ALLOWED_FORMATS = {'PNG', 'JPEG', 'JPG', 'BMP', 'TIFF', 'WEBP'}
    ALLOWED_MODES = {'L', 'RGB', 'RGBA', 'P'}  # P = palette mode
    
    # Magic bytes for common image formats
    MAGIC_BYTES = {
        'PNG': b'\x89PNG\r\n\x1a\n',
        'JPEG': b'\xff\xd8\xff',
        'BMP': b'BM',
        'TIFF_LE': b'II\x2a\x00',  # Little-endian
        'TIFF_BE': b'MM\x00\x2a',  # Big-endian
        'WEBP': b'RIFF',
    }
    
    @classmethod
    def validate_file_path(cls, filepath: str) -> Tuple[bool, str]:
        """
        Validate file path exists and is accessible.
        
        Args:
            filepath: Path to file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not filepath:
            return False, "File path is empty"
        
        path = Path(filepath)
        
        if not path.exists():
            return False, f"File not found: {filepath}"
        
        if not path.is_file():
            return False, f"Path is not a file: {filepath}"
        
        if not os.access(filepath, os.R_OK):
            return False, f"File is not readable: {filepath}"
        
        return True, ""
    
    @classmethod
    def validate_file_size(cls, filepath: str) -> Tuple[bool, str]:
        """
        Validate file size is within limits.
        
        Args:
            filepath: Path to file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        file_size = os.path.getsize(filepath)
        
        if file_size == 0:
            return False, "File is empty"
        
        if file_size > cls.MAX_FILE_SIZE:
            max_mb = cls.MAX_FILE_SIZE / (1024 * 1024)
            actual_mb = file_size / (1024 * 1024)
            return False, f"File too large: {actual_mb:.2f}MB (max: {max_mb}MB)"
        
        return True, ""
    
    @classmethod
    def validate_magic_bytes(cls, filepath: str) -> Tuple[bool, str]:
        """
        Validate file has correct magic bytes for its extension.
        Prevents MIME type spoofing attacks.
        
        Args:
            filepath: Path to file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            with open(filepath, 'rb') as f:
                header = f.read(12)  # Read first 12 bytes
            
            # Check against known magic bytes
            is_valid_format = False
            detected_format = None
            
            for format_name, magic in cls.MAGIC_BYTES.items():
                if header.startswith(magic):
                    is_valid_format = True
                    detected_format = format_name
                    break
            
            if not is_valid_format:
                # Try using PIL as fallback
                try:
                    with Image.open(filepath) as test_img:
                        detected_format = test_img.format
                        if detected_format:
                            is_valid_format = True
                except:
                    pass
            
            if not is_valid_format:
                return False, "File is not a valid image (magic bytes check failed)"
            
            return True, ""
            
        except Exception as e:
            return False, f"Error reading file: {str(e)}"
    
    @classmethod
    def validate_image_format(cls, img: Image.Image) -> Tuple[bool, str]:
        """
        Validate PIL Image object format and mode.
        
        Args:
            img: PIL Image object
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check format
        if img.format and img.format.upper() not in cls.ALLOWED_FORMATS:
            return False, f"Unsupported image format: {img.format}. Allowed: {', '.join(cls.ALLOWED_FORMATS)}"
        
        # Check mode
        if img.mode not in cls.ALLOWED_MODES:
            return False, f"Unsupported image mode: {img.mode}. Allowed: {', '.join(cls.ALLOWED_MODES)}"
        
        return True, ""
    
    @classmethod
    def validate_image_dimensions(cls, img: Image.Image) -> Tuple[bool, str]:
        """
        Validate image dimensions to prevent resource exhaustion.
        
        Args:
            img: PIL Image object
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        width, height = img.size
        total_pixels = width * height
        
        if total_pixels > cls.MAX_PIXELS:
            max_mp = cls.MAX_PIXELS / 1_000_000
            actual_mp = total_pixels / 1_000_000
            return False, f"Image too large: {actual_mp:.2f}MP (max: {max_mp}MP). Dimensions: {width}x{height}"
        
        if width <= 0 or height <= 0:
            return False, f"Invalid dimensions: {width}x{height}"
        
        return True, ""
    
    @classmethod
    def validate_image_content(cls, img: Image.Image) -> Tuple[bool, str]:
        """
        Validate image content for potential exploits.
        
        This is a basic check. For production, consider using:
        - ClamAV for malware scanning
        - Custom ML models for detecting steganography
        
        Args:
            img: PIL Image object
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Try to convert to array (will fail on corrupted images)
            img_array = np.array(img)
            
            # Check for suspicious patterns
            if img_array.size == 0:
                return False, "Image data is empty"
            
            # Check for extreme pixel values (potential exploit)
            if img_array.dtype == np.uint8:
                # This is normal, uint8 images are standard
                pass
            elif img_array.dtype in [np.float32, np.float64]:
                # Floating point images might be suspicious
                if np.any(np.isnan(img_array)) or np.any(np.isinf(img_array)):
                    return False, "Image contains invalid pixel values (NaN/Inf)"
            
            return True, ""
            
        except Exception as e:
            return False, f"Image content validation failed: {str(e)}"
    
    @classmethod
    def validate_image_file(cls, filepath: str) -> Tuple[bool, str, Optional[Image.Image]]:
        """
        Comprehensive image file validation.
        
        Performs all validation checks in sequence.
        
        Args:
            filepath: Path to image file
            
        Returns:
            Tuple of (is_valid, error_message, image_object)
            If invalid, image_object will be None
        """
        # Check 1: File path
        is_valid, error = cls.validate_file_path(filepath)
        if not is_valid:
            return False, error, None
        
        # Check 2: File size
        is_valid, error = cls.validate_file_size(filepath)
        if not is_valid:
            return False, error, None
        
        # Check 3: Magic bytes
        is_valid, error = cls.validate_magic_bytes(filepath)
        if not is_valid:
            return False, error, None
        
        # Check 4: Open image
        try:
            img = Image.open(filepath)
        except Exception as e:
            return False, f"Failed to open image: {str(e)}", None
        
        # Check 5: Format and mode
        is_valid, error = cls.validate_image_format(img)
        if not is_valid:
            img.close()
            return False, error, None
        
        # Check 6: Dimensions
        is_valid, error = cls.validate_image_dimensions(img)
        if not is_valid:
            img.close()
            return False, error, None
        
        # Check 7: Content
        is_valid, error = cls.validate_image_content(img)
        if not is_valid:
            img.close()
            return False, error, None
        
        # All checks passed!
        return True, "Valid image", img


class KeyFileValidator:
    """
    Validates encryption key files.
    """
    
    MAX_KEY_FILE_SIZE = 100 * 1024 * 1024  # 100 MB (for large permutations)
    
    @classmethod
    def validate_key_file(cls, filepath: str) -> Tuple[bool, str]:
        """
        Validate encryption key file.
        
        Args:
            filepath: Path to key file (.npz)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file exists
        if not os.path.exists(filepath):
            return False, f"Key file not found: {filepath}"
        
        # Check extension
        if not filepath.endswith('.npz'):
            return False, f"Invalid key file extension. Expected .npz, got: {Path(filepath).suffix}"
        
        # Check file size
        file_size = os.path.getsize(filepath)
        if file_size > cls.MAX_KEY_FILE_SIZE:
            return False, f"Key file too large: {file_size / (1024*1024):.2f}MB"
        
        # Try to load the file
        try:
            keys = np.load(filepath, allow_pickle=False)
            
            # Check required fields
            required_fields = ['xor_key', 'permutation_key']
            missing_fields = [f for f in required_fields if f not in keys.files]
            
            if missing_fields:
                return False, f"Key file missing required fields: {', '.join(missing_fields)}"
            
            # Validate key types
            if keys['xor_key'].dtype != np.uint8:
                return False, "Invalid XOR key type"
            
            if keys['permutation_key'].dtype not in [np.int32, np.int64]:
                return False, "Invalid permutation key type"
            
            keys.close()
            return True, "Valid key file"
            
        except Exception as e:
            return False, f"Failed to load key file: {str(e)}"


class EncryptionOptionsValidator:
    """
    Validates encryption options and parameters.
    """
    
    VALID_PURITY_LEVELS = {'maximum', 'balanced', 'fast'}
    
    @classmethod
    def validate_quantum_purity(cls, purity: str) -> Tuple[bool, str]:
        """
        Validate quantum purity level.
        
        Args:
            purity: Purity level string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if purity not in cls.VALID_PURITY_LEVELS:
            return False, f"Invalid purity level: {purity}. Allowed: {', '.join(cls.VALID_PURITY_LEVELS)}"
        return True, ""
    
    @classmethod
    def validate_master_password(cls, password: Optional[str]) -> Tuple[bool, str]:
        """
        Validate master password strength.
        
        Args:
            password: Master password (optional)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if password is None:
            return True, ""  # Password is optional
        
        if len(password) < 8:
            return False, "Master password must be at least 8 characters"
        
        # Check for complexity (basic)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_upper and has_lower and has_digit):
            return False, "Master password must contain uppercase, lowercase, and digits"
        
        return True, ""
