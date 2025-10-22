"""
Command-Line Interface for Quantum-Seed ImageShield

Provides easy-to-use commands for encrypting and decrypting images.
"""

import argparse
import sys
from .encryption import ImageEncryptor
from .decryption import ImageDecryptor


def encrypt_command(args):
    """Execute the encryption command."""
    encryptor = ImageEncryptor(quantum_seed=args.seed)
    
    key_path = args.key if args.key else args.output.replace('.png', '_keys.npz').replace('.jpg', '_keys.npz')
    
    print(f"Encrypting image: {args.input}")
    print("Generating quantum random keys...")
    
    xor_key, permutation_key = encryptor.encrypt_image(
        args.input, 
        args.output, 
        key_path
    )
    
    print(f"Encryption complete!")
    print(f"Encrypted image saved to: {args.output}")
    print(f"Keys saved to: {key_path}")
    print(f"XOR key length: {len(xor_key)} bytes")
    print(f"Permutation size: {len(permutation_key)} elements")


def decrypt_command(args):
    """Execute the decryption command."""
    decryptor = ImageDecryptor()
    
    if not args.key:
        print("Error: Key file path is required for decryption", file=sys.stderr)
        sys.exit(1)
    
    print(f"Decrypting image: {args.input}")
    print(f"Loading keys from: {args.key}")
    
    decryptor.decrypt_image(
        args.input,
        args.output,
        key_path=args.key
    )
    
    print(f"Decryption complete!")
    print(f"Decrypted image saved to: {args.output}")


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
