"""
Command-Line Interface for Quantum-Seed ImageShield

Provides easy-to-use commands for encrypting and decrypting images.
"""

import argparse
import sys
from .encryption import ImageEncryptor
from .decryption import ImageDecryptor
from .validators import ImageValidator, KeyFileValidator, EncryptionOptionsValidator


def encrypt_command(args):
    """Execute the encryption command."""
    # Validate purity level
    purity = args.purity if hasattr(args, 'purity') and args.purity else 'balanced'
    is_valid, error = EncryptionOptionsValidator.validate_quantum_purity(purity)
    if not is_valid:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    
    # Validate input image
    print(f"Validating input image: {args.input}")
    is_valid, error, img = ImageValidator.validate_image_file(args.input)
    if not is_valid:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    img.close()  # Close the validation image
    
    # Create encryptor
    encryptor = ImageEncryptor(quantum_seed=args.seed, quantum_purity=purity)
    
    key_path = args.key if args.key else args.output.replace('.png', '_keys.npz').replace('.jpg', '_keys.npz')
    
    print(f"Encrypting image: {args.input}")
    print(f"Quantum purity level: {purity}")
    if purity == 'maximum':
        print("⚠️  Using MAXIMUM purity - this may take several minutes for large images")
    print("Generating quantum random keys...")
    
    try:
        xor_key, permutation_key = encryptor.encrypt_image(
            args.input, 
            args.output, 
            key_path
        )
        
        print(f"✅ Encryption complete!")
        print(f"Encrypted image saved to: {args.output}")
        print(f"Keys saved to: {key_path}")
        print(f"XOR key length: {len(xor_key)} bytes")
        print(f"Permutation size: {len(permutation_key)} elements")
        print(f"Quantum purity: {purity}")
        
    except Exception as e:
        print(f"❌ Encryption failed: {str(e)}", file=sys.stderr)
        sys.exit(1)


def decrypt_command(args):
    """Execute the decryption command."""
    if not args.key:
        print("Error: Key file path is required for decryption", file=sys.stderr)
        sys.exit(1)
    
    # Validate key file
    print(f"Validating key file: {args.key}")
    is_valid, error = KeyFileValidator.validate_key_file(args.key)
    if not is_valid:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    
    # Validate encrypted image
    print(f"Validating encrypted image: {args.input}")
    is_valid, error, img = ImageValidator.validate_image_file(args.input)
    if not is_valid:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    img.close()
    
    decryptor = ImageDecryptor()
    
    print(f"Decrypting image: {args.input}")
    print(f"Loading keys from: {args.key}")
    
    try:
        decryptor.decrypt_image(
            args.input,
            args.output,
            key_path=args.key
        )
        
        print(f"✅ Decryption complete!")
        print(f"Decrypted image saved to: {args.output}")
        
    except Exception as e:
        print(f"❌ Decryption failed: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Quantum-Seed ImageShield: Hybrid Quantum-Classical Image Encryption"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt an image')
    encrypt_parser.add_argument('input', help='Path to input image')
    encrypt_parser.add_argument('output', help='Path to save encrypted image')
    encrypt_parser.add_argument('--key', '-k', help='Path to save encryption keys')
    encrypt_parser.add_argument('--seed', '-s', type=int, help='Quantum seed for reproducibility (optional)')
    encrypt_parser.add_argument(
        '--purity', '-p', 
        choices=['maximum', 'balanced', 'fast'],
        default='balanced',
        help='Quantum purity level: maximum (slowest, most secure), balanced (recommended), fast (development)'
    )
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt an image')
    decrypt_parser.add_argument('input', help='Path to encrypted image')
    decrypt_parser.add_argument('output', help='Path to save decrypted image')
    decrypt_parser.add_argument('--key', '-k', required=True, help='Path to encryption keys')
    
    args = parser.parse_args()
    
    if args.command == 'encrypt':
        encrypt_command(args)
    elif args.command == 'decrypt':
        decrypt_command(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
