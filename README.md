# Quantum-Seed ImageShield

Hybrid quantum–classical image encryption prototype.

## Overview
Quantum-Seed ImageShield uses Qiskit to generate true-random bits (Hadamard + measure) which are then used to create a keystream (for XOR) and a permutation seed (for pixel shuffling). The system encrypts grayscale images and supports lossless decryption.

## How to run
1. Create a virtual environment and install requirements:

```bash
python -m venv venv
source venv/bin/activate    # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

2. Run tests:

```bash
python test_example.py --input sample.png
```

3. Run the Streamlit demo:

```bash
streamlit run app.py
```

## Notes
- Qiskit Aer is used as a simulator backend for quantum randomness. If Aer isn't available you'll get a cryptographically weaker fallback PRNG for development only.
- Start with small grayscale images (e.g., 128x128) while testing.
