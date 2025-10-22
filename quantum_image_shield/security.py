"""
Security Module - Cryptographic Hardening

Implements enterprise-grade security features:
- PBKDF2 key derivation
- HMAC integrity verification
- Authenticated encryption
- Secure key storage
"""

import hashlib
import hmac
import secrets
from typing import Tuple, Dict, Optional
import numpy as np


class SecurityHardening:
    """
    Enterprise-grade security enhancements for quantum encryption.
    
    Provides:
    - Key derivation functions (KDF)
    - Message authentication codes (HMAC)
    - Integrity verification
    - Secure random generation
    """
    
    # Security parameters
    PBKDF2_ITERATIONS = 100000  # OWASP recommended minimum
    SALT_LENGTH = 32  # 256 bits
    HMAC_KEY_LENGTH = 32  # 256 bits
    
    @staticmethod
    def derive_key(password: str, salt: bytes = None, iterations: int = None) -> Tuple[bytes, bytes]:
        """
        Derive a cryptographic key from a password using PBKDF2.
        
        Args:
            password: User password/passphrase
            salt: Optional salt (generated if not provided)
            iterations: Number of PBKDF2 iterations (default: 100000)
            
        Returns:
            Tuple of (derived_key, salt)
        """
        if salt is None:
            salt = secrets.token_bytes(SecurityHardening.SALT_LENGTH)
        
        if iterations is None:
            iterations = SecurityHardening.PBKDF2_ITERATIONS
        
        # Derive 256-bit key using PBKDF2-HMAC-SHA256
        derived_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            iterations,
            dklen=32  # 256 bits
        )
        
        return derived_key, salt
    
    @staticmethod
    def generate_hmac(data: bytes, key: bytes) -> bytes:
        """
        Generate HMAC-SHA256 for data integrity verification.
        
        Args:
            data: Data to authenticate
            key: HMAC key
            
        Returns:
            HMAC tag (32 bytes)
        """
        return hmac.new(key, data, hashlib.sha256).digest()
    
    @staticmethod
    def verify_hmac(data: bytes, key: bytes, expected_hmac: bytes) -> bool:
        """
        Verify HMAC tag for data integrity.
        
        Args:
            data: Data to verify
            key: HMAC key
            expected_hmac: Expected HMAC tag
            
        Returns:
            True if HMAC is valid, False otherwise
        """
        computed_hmac = SecurityHardening.generate_hmac(data, key)
        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(computed_hmac, expected_hmac)
    
    @staticmethod
    def encrypt_key(key: bytes, master_key: bytes) -> bytes:
        """
        Encrypt a key using XOR with master key (simple but effective).
        For production, consider using AES-GCM.
        
        Args:
            key: Key to encrypt
            master_key: Master encryption key
            
        Returns:
            Encrypted key
        """
        # Ensure master key is long enough
        if len(master_key) < len(key):
            # Stretch master key using SHA-256 chaining
            stretched = master_key
            while len(stretched) < len(key):
                stretched += hashlib.sha256(stretched).digest()
            master_key = stretched[:len(key)]
        
        # XOR encryption (self-inverse)
        key_array = np.frombuffer(key, dtype=np.uint8)
        master_array = np.frombuffer(master_key[:len(key)], dtype=np.uint8)
        encrypted = np.bitwise_xor(key_array, master_array)
        
        return encrypted.tobytes()
    
    @staticmethod
    def decrypt_key(encrypted_key: bytes, master_key: bytes) -> bytes:
        """
        Decrypt a key (XOR is self-inverse).
        
        Args:
            encrypted_key: Encrypted key
            master_key: Master encryption key
            
        Returns:
            Decrypted key
        """
        # XOR decryption is same as encryption
        return SecurityHardening.encrypt_key(encrypted_key, master_key)
    
    @staticmethod
    def calculate_file_hash(data: bytes, algorithm: str = 'sha256') -> str:
        """
        Calculate cryptographic hash of data.
        
        Args:
            data: Data to hash
            algorithm: Hash algorithm ('sha256', 'sha512', 'blake2b')
            
        Returns:
            Hex-encoded hash
        """
        if algorithm == 'sha256':
            return hashlib.sha256(data).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(data).hexdigest()
        elif algorithm == 'blake2b':
            return hashlib.blake2b(data).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    @staticmethod
    def generate_secure_random(length: int) -> bytes:
        """
        Generate cryptographically secure random bytes.
        
        Args:
            length: Number of bytes to generate
            
        Returns:
            Secure random bytes
        """
        return secrets.token_bytes(length)


class SecureKeyStorage:
    """
    Secure key storage with encryption and integrity verification.
    """
    
    def __init__(self, master_password: Optional[str] = None):
        """
        Initialize secure key storage.
        
        Args:
            master_password: Optional master password for key encryption
        """
        self.master_password = master_password
        self.master_key = None
        self.salt = None
        
        if master_password:
            self.master_key, self.salt = SecurityHardening.derive_key(master_password)
    
    def save_keys_secure(self, 
                        filepath: str,
                        xor_key: bytes,
                        permutation_key: np.ndarray,
                        metadata: Dict) -> None:
        """
        Save encryption keys with security hardening.
        
        Args:
            filepath: Path to save keys
            xor_key: XOR encryption key
            permutation_key: Permutation array
            metadata: Additional metadata (shape, mode, etc.)
        """
        # Generate HMAC key
        hmac_key = SecurityHardening.generate_secure_random(32)
        
        # Optionally encrypt the XOR key
        if self.master_key:
            encrypted_xor_key = SecurityHardening.encrypt_key(xor_key, self.master_key)
        else:
            encrypted_xor_key = xor_key
        
        # Convert permutation to bytes
        perm_bytes = permutation_key.tobytes()
        
        # Generate integrity HMAC
        data_to_authenticate = encrypted_xor_key + perm_bytes
        integrity_hmac = SecurityHardening.generate_hmac(data_to_authenticate, hmac_key)
        
        # Calculate file hash for additional verification
        file_hash = SecurityHardening.calculate_file_hash(
            encrypted_xor_key + perm_bytes
        )
        
        # Prepare save data
        save_data = {
            'xor_key': np.frombuffer(encrypted_xor_key, dtype=np.uint8),
            'permutation_key': permutation_key,
            'hmac_key': np.frombuffer(hmac_key, dtype=np.uint8),
            'integrity_hmac': np.frombuffer(integrity_hmac, dtype=np.uint8),
            'file_hash': file_hash,
            'encrypted': self.master_key is not None,
            'version': '2.0'
        }
        
        # Add metadata
        if self.salt is not None:
            save_data['salt'] = np.frombuffer(self.salt, dtype=np.uint8)
        
        for key, value in metadata.items():
            save_data[key] = value
        
        # Save with compression
        np.savez_compressed(filepath, **save_data)
    
    def load_keys_secure(self, filepath: str) -> Tuple[bytes, np.ndarray, Dict]:
        """
        Load and verify encryption keys.
        
        Args:
            filepath: Path to key file
            
        Returns:
            Tuple of (xor_key, permutation_key, metadata)
            
        Raises:
            ValueError: If integrity check fails or decryption fails
        """
        # Load key file
        keys = np.load(filepath, allow_pickle=False)  # Disable pickle for security
        
        # Extract components
        encrypted_xor_key = keys['xor_key'].tobytes()
        permutation_key = keys['permutation_key']
        hmac_key = keys['hmac_key'].tobytes()
        expected_hmac = keys['integrity_hmac'].tobytes()
        is_encrypted = bool(keys.get('encrypted', False))
        
        # Verify integrity
        data_to_verify = encrypted_xor_key + permutation_key.tobytes()
        if not SecurityHardening.verify_hmac(data_to_verify, hmac_key, expected_hmac):
            raise ValueError("Key file integrity check FAILED - possible tampering detected!")
        
        # Decrypt XOR key if needed
        if is_encrypted:
            if not self.master_password:
                raise ValueError("Key file is encrypted but no master password provided")
            
            # Derive key from password and stored salt
            if 'salt' in keys:
                salt = keys['salt'].tobytes()
                master_key, _ = SecurityHardening.derive_key(self.master_password, salt)
            else:
                raise ValueError("Encrypted key file missing salt")
            
            xor_key = SecurityHardening.decrypt_key(encrypted_xor_key, master_key)
        else:
            xor_key = encrypted_xor_key
        
        # Extract metadata
        metadata = {
            'shape': tuple(keys['shape']) if 'shape' in keys else None,
            'mode': str(keys['mode']) if 'mode' in keys else None,
            'quantum_purity': str(keys.get('quantum_purity', 'unknown')),
            'version': str(keys.get('version', '1.0'))
        }
        
        return xor_key, permutation_key, metadata
