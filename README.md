# Quantum-Seed ImageShield

A hybrid quantum-classical image encryption system that leverages quantum-generated randomness to enhance security and unpredictability in digital image encryption.

## Overview

Quantum-Seed ImageShield combines quantum key generation using **Qiskit** with classical encryption techniques to create a robust image encryption system. The system demonstrates a practical application of quantum computing in modern cryptography by:

- **Quantum Key Generation**: Using quantum circuits with superposition states to generate truly random keys
- **XOR Encryption**: Applying bitwise XOR operations with quantum-generated keys
- **Pixel Permutation**: Shuffling pixels based on quantum randomness for additional security

## Features

✨ **True Quantum Randomness**: Keys are generated using quantum measurements of superposition states  
🔐 **Hybrid Encryption**: Combines quantum and classical techniques for robust security  
🖼️ **Lossless Encryption**: Perfect recovery of original images after decryption  
🎨 **Format Support**: Works with various image formats (PNG, JPEG, etc.)  
🧪 **Fully Tested**: Comprehensive test suite included  
📦 **Easy to Use**: Simple CLI and Python API

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

The main dependencies are:
- `qiskit`: Quantum computing framework
- `qiskit-aer`: Quantum circuit simulator
- `numpy`: Numerical operations
- `pillow`: Image processing

## Usage

### Command-Line Interface

#### Encrypt an Image

```bash
python -m quantum_image_shield.cli encrypt input.png encrypted.png
```

This will:
- Encrypt the image using quantum-generated keys
- Save the encrypted image to `encrypted.png`
- Save encryption keys to `encrypted_keys.npz`

You can also specify a custom key file location:

```bash
python -m quantum_image_shield.cli encrypt input.png encrypted.png --key my_keys.npz
```

#### Decrypt an Image

```bash
python -m quantum_image_shield.cli decrypt encrypted.png decrypted.png --key encrypted_keys.npz
```

### Python API

```python
from quantum_image_shield import ImageEncryptor, ImageDecryptor

# Encrypt an image
encryptor = ImageEncryptor()
xor_key, permutation_key = encryptor.encrypt_image(
    'input.png',
    'encrypted.png',
    'keys.npz'
)

# Decrypt the image
decryptor = ImageDecryptor()
decryptor.decrypt_image(
    'encrypted.png',
    'decrypted.png',
    key_path='keys.npz'
)
```

### Example Script

Run the included example to see the system in action:

```bash
cd examples
python example_usage.py
```

This will:
1. Create a sample image
2. Encrypt it using quantum-generated keys
3. Decrypt it back to the original
4. Verify the encryption/decryption cycle

## How It Works

### 1. Quantum Key Generation

The system uses Qiskit to create quantum circuits with Hadamard gates, which put qubits into superposition states. When measured, these qubits collapse to either 0 or 1 with true randomness:

```
|0⟩ --[H]-- → (|0⟩ + |1⟩)/√2 --[Measure]-- → 0 or 1 (50% probability)
```

This quantum randomness is used to generate:
- **XOR keys**: Random byte sequences for encryption
- **Permutation keys**: Random shuffling patterns for pixels

### 2. Classical Encryption

The classical encryption process involves two steps:

**Step 1: XOR Encryption**
- Each pixel value is XORed with a quantum-generated key byte
- This provides the primary encryption layer

**Step 2: Pixel Permutation**
- Pixels are shuffled according to a quantum-generated permutation
- This adds confusion and diffusion to the encrypted image

### 3. Decryption

Decryption reverses the process:
1. **Unpermute**: Restore original pixel positions
2. **XOR**: Apply the same XOR key (XOR is self-inverse)

## Architecture

```
quantum_image_shield/
├── __init__.py                    # Package initialization
├── quantum_key_generator.py       # Quantum key generation using Qiskit
├── encryption.py                  # Image encryption module
├── decryption.py                  # Image decryption module
└── cli.py                         # Command-line interface

tests/
├── test_quantum_key_generator.py  # Tests for quantum key generation
└── test_encryption_decryption.py  # Tests for encryption/decryption

examples/
└── example_usage.py               # Example usage demonstration
```

## Security Considerations

- **Key Storage**: Encryption keys must be stored securely. Without the keys, decryption is not possible.
- **Quantum Randomness**: True randomness from quantum measurements provides superior unpredictability compared to classical PRNGs.
- **XOR Security**: XOR encryption is secure when used with truly random keys that are as long as the data.
- **Permutation**: Adds an additional layer of security through pixel shuffling.

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_quantum_key_generator.py

# Run with verbose output
python -m pytest -v tests/

# Run with unittest
python -m unittest discover tests/
```

## Requirements

See `requirements.txt` for all dependencies:
- qiskit >= 0.45.0
- qiskit-aer >= 0.13.0
- numpy >= 1.24.0
- pillow >= 10.0.0

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available for educational and research purposes.

## Acknowledgments

- **Qiskit**: IBM's quantum computing framework
- Quantum computing community for advancing quantum cryptography research

## Future Enhancements

Potential areas for expansion:
- Quantum key distribution (QKD) integration
- Support for video encryption
- Hardware quantum computer integration
- Additional classical encryption algorithms
- Performance optimizations for large images

---

**Note**: This project demonstrates the practical application of quantum computing in cryptography. While the system uses quantum-generated randomness for enhanced security, it should be evaluated by security experts before use in production environments.