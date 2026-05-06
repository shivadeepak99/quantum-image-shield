# 🔐 Quantum-Seed ImageShield

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Qiskit](https://img.shields.io/badge/Qiskit-1.2-6929C4.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39-FF4B4B.svg)
![Tests](https://img.shields.io/badge/tests-14%2F14%20passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Hybrid quantum-classical image encryption — quantum-generated keys, classical XOR + permutation, perfect reconstruction.**

</div>

---

## Overview

Quantum-Seed ImageShield uses IBM's **Qiskit** to generate cryptographic keys through quantum circuits (Hadamard gates → superposition → measurement → true random bits), then applies classical encryption techniques to protect images. The result: statistically provable encryption quality with entropy near the theoretical maximum of 8 bits.

This is a full-stack demo: a Python cryptography core + a **Streamlit web app** for interactive encrypt/decrypt/analysis.

---

## How It Works

```
Input Image (grayscale)
        │
        ▼
Quantum Key Generation          ← Qiskit AerSimulator + Hadamard gates
  · XOR keystream (N bytes)
  · Permutation seed (32-bit)
        │
        ▼
Encryption
  1. XOR each pixel with keystream
  2. Permute pixel positions with quantum seed
        │
        ▼
Encrypted Image  ──────────────────────────────────┐
                                                   │
Decryption (same keys, reverse order)             │
  1. Inverse permutation                          │
  2. XOR again (XOR is self-inverse)              │
        │                                         │
        ▼                                         │
Decrypted Image ← PSNR = ∞ (perfect match) ◄─────┘
```

**Encryption quality metrics measured:** Shannon entropy, histogram uniformity, pixel correlation (H/V/diagonal), PSNR.

---

## Quick Start

### Requirements

- Python 3.8+
- No IBM Quantum account needed — runs on the local **AerSimulator**

### Install

```bash
git clone https://github.com/shivadeepak99/quantum-image-shield.git
cd quantum-image-shield
pip install -r requirements.txt
```

### Run tests (14/14 passing)

```bash
pytest tests/ -v
```

### E2E demo (CLI)

```bash
# Generate a sample image and run full encrypt/decrypt/analysis cycle
python test_encryption.py
```

Output:
```
✓ Entropy increased by: 0.4612 bits
✓ Average correlation decreased by: 0.9896
✓ Uniformity improved: True
✓ Decryption: PERFECT ✓ (PSNR = ∞)
```

### Web App

```bash
streamlit run app.py
```

Then open **http://localhost:8501** — upload any image, generate quantum keys, encrypt, decrypt, and inspect the statistical analysis side-by-side.

---

## Project Structure

```
quantum-image-shield/
├── app.py                      # Streamlit web interface
├── quantum_key_generator.py    # Quantum key generation (Qiskit + AerSimulator)
├── image_encryptor.py          # XOR + permutation encrypt/decrypt
├── image_analysis.py           # Entropy, uniformity, correlation, PSNR
├── generate_sample_image.py    # Creates samples/sample_image.png for testing
├── test_encryption.py          # CLI end-to-end demo script
├── tests/
│   ├── test_quantum_key_generator.py   # Unit tests — key generation
│   └── test_encryption_decryption.py  # Unit tests — encrypt/decrypt cycle
├── samples/                    # Runtime output directory (auto-created)
└── requirements.txt
```

---

## Encryption Quality Results

On a 256×256 grayscale test image:

| Metric | Original | Encrypted | Change |
|--------|----------|-----------|--------|
| Entropy (bits) | 7.533 | 7.994 | +0.46 ↑ |
| Histogram Uniformity | 0.792 | 0.999 | +0.21 ↑ |
| Avg Pixel Correlation | 0.987 | ~0.000 | −0.99 ↓ |
| PSNR after decrypt | — | — | ∞ (perfect) |

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `qiskit` | 1.2.4 | Quantum circuit construction |
| `qiskit-aer` | 0.15.1 | Local quantum simulator |
| `numpy` | 1.26.4 | Array operations |
| `pillow` | 10.4.0 | Image I/O |
| `matplotlib` | 3.9.2 | Histogram / correlation plots |
| `streamlit` | 1.39.0 | Web interface |
| `scipy` | 1.14.1 | Shannon entropy calculation |

No IBM Quantum account or API key required — `AerSimulator` runs entirely locally.

---

## Security Notes

- This is a **demonstration project** — not production cryptography
- XOR with a random keystream is a one-time pad if the key is truly random and never reused; the quantum source provides that property in simulation
- The key file (`.npz`) is required for decryption — keep it secret
- For production use, replace AerSimulator with a real quantum hardware backend or a NIST-certified CSPRNG

---

## License

MIT — see [LICENSE](LICENSE)
