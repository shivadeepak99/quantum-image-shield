# 🔐 Quantum-Seed ImageShield

A hybrid quantum-classical image encryption system that leverages quantum-generated randomness to enhance security and unpredictability in digital image encryption.

## 🌟 Overview

**Quantum-Seed ImageShield** combines quantum key generation using IBM's Qiskit platform with classical encryption techniques (XOR operations and pixel permutations) to demonstrate a practical application of quantum computing in modern cryptography.

### Key Features

- 🔬 **Quantum Key Generation**: Uses Hadamard gates and measurements to generate truly random cryptographic keys
- 🔐 **Hybrid Encryption**: Combines XOR operations with quantum keystreams and pixel permutation
- 📊 **Comprehensive Analysis**: Evaluates encryption quality through entropy, histogram uniformity, correlation, and PSNR metrics
- 🎨 **Interactive Demo**: User-friendly Streamlit interface for visualizing encryption/decryption process
- ✅ **Reversible**: Perfect reconstruction of original images after decryption

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Input Image                          │
│                  (Grayscale)                            │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│             Quantum Key Generation                      │
│   (Qiskit - Hadamard Gates + Measurements)              │
│   - Generates random keystream                          │
│   - Generates permutation seed                          │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                  Encryption                             │
│   1. XOR with quantum keystream                         │
│   2. Pixel permutation                                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│               Encrypted Image                           │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/shivadeepak99/quantum-image-shield.git
cd quantum-image-shield
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Command Line Interface

1. Generate a sample image:
```bash
python generate_sample_image.py
```

2. Run the test suite:
```bash
python test_encryption.py
```

This will:
- Load/generate a sample image
- Generate quantum keys using Qiskit
- Encrypt the image
- Decrypt the image
- Verify perfect reconstruction
- Display comprehensive analysis metrics

### Web Interface (Streamlit)

Launch the interactive demo:
```bash
streamlit run app.py
```

The web interface allows you to:
- Upload your own images
- Generate quantum keys and encrypt images
- Decrypt images and verify reconstruction
- View detailed statistical analysis
- Compare histograms and correlation plots
- Analyze encryption quality metrics

## 📊 Encryption Quality Metrics

The system evaluates encryption quality through several metrics:

### 1. **Entropy**
- Measures randomness in pixel values
- Higher entropy (closer to 8 bits) indicates better encryption
- Expected: Significant increase after encryption

### 2. **Histogram Uniformity**
- Measures how evenly pixel values are distributed
- Range: 0 to 1 (1 = perfectly uniform)
- Expected: More uniform distribution after encryption

### 3. **Correlation Coefficient**
- Measures similarity between adjacent pixels
- Range: -1 to 1 (0 = no correlation)
- Calculated for horizontal, vertical, and diagonal directions
- Expected: Near-zero correlation after encryption

### 4. **PSNR (Peak Signal-to-Noise Ratio)**
- Measures quality of decrypted image vs. original
- Higher is better; ∞ means perfect reconstruction
- Expected: ∞ (perfect reconstruction)

## 🔬 Technical Details

### Quantum Key Generation

The system uses quantum circuits to generate truly random keys:

1. **Circuit Construction**: Creates quantum circuits with Hadamard gates
2. **Superposition**: Applies Hadamard gates to put qubits in superposition
3. **Measurement**: Measures qubits to collapse superposition into random bits
4. **Key Derivation**: Converts random bits into keystream and permutation seed

### Encryption Process

1. **XOR Operation**: Each pixel is XORed with corresponding keystream byte
2. **Pixel Permutation**: Pixels are shuffled using quantum-derived seed
3. **Result**: Encrypted image with high entropy and low correlation

### Decryption Process

1. **Reverse Permutation**: Pixels are unshuffled using the same seed
2. **XOR Operation**: Applied again (XOR is self-inverse)
3. **Result**: Perfect reconstruction of original image

## 📁 Project Structure

```
quantum-image-shield/
├── app.py                      # Streamlit web interface
├── quantum_key_generator.py    # Quantum key generation module
├── image_encryptor.py          # Encryption/decryption module
├── image_analysis.py           # Statistical analysis module
├── test_encryption.py          # Test suite
├── generate_sample_image.py    # Sample image generator
├── requirements.txt            # Python dependencies
├── samples/                    # Sample images directory
│   ├── sample_image.png
│   ├── encrypted_image.png
│   └── decrypted_image.png
└── README.md                   # This file
```

## 🎯 Expected Results

A well-encrypted image should exhibit:

- ✅ **High Entropy**: Close to 8 bits (maximum for 8-bit images)
- ✅ **Uniform Histogram**: Flat distribution across all pixel values
- ✅ **Low Correlation**: Near-zero correlation between adjacent pixels
- ✅ **Perfect Decryption**: PSNR = ∞ (identical to original)

## 🔐 Security Considerations

- Uses quantum-generated randomness for enhanced unpredictability
- XOR encryption provides confusion (scrambles pixel values)
- Permutation provides diffusion (spreads information across image)
- Keys must be kept secret and transmitted securely
- Same key required for decryption (symmetric encryption)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- IBM Qiskit team for quantum computing framework
- Quantum computing research community
- Classical cryptography principles

## 📚 References

- Qiskit Documentation: https://qiskit.org/
- Quantum Random Number Generation
- Image Encryption Techniques
- Cryptographic Analysis Methods

---

**Note**: This is a demonstration project showcasing the intersection of quantum computing, cybersecurity, and digital imaging. For production use, additional security measures and key management protocols should be implemented.