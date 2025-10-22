# Usage Guide - Quantum-Seed ImageShield

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/shivadeepak99/quantum-image-shield.git
cd quantum-image-shield

# Install dependencies
pip install -r requirements.txt
```

### 2. Command Line Usage

#### Generate Sample Image

```bash
python generate_sample_image.py
```

This creates a test image at `samples/sample_image.png`.

#### Run Complete Test

```bash
python test_encryption.py
```

This will:
- Load or generate a sample image
- Generate quantum keys using Qiskit
- Encrypt the image
- Decrypt the image
- Verify perfect reconstruction
- Display comprehensive metrics

**Expected Output:**
```
============================================================
Quantum-Seed ImageShield - Test Suite
============================================================

1. Loading sample image...
   ✓ Image loaded: 256x256 pixels

2. Generating quantum keys...
   ✓ Keystream generated: 65536 bytes
   ✓ Permutation seed: 3927935018

3. Encrypting image...
   ✓ Image encrypted successfully
   ✓ Encrypted image saved: samples/encrypted_image.png

4. Decrypting image...
   ✓ Image decrypted successfully
   ✓ Decrypted image saved: samples/decrypted_image.png

5. Verifying decryption...
   ✓ Perfect reconstruction! PSNR = ∞
   ✓ Original and decrypted images are identical

6. Analyzing images...
   [Detailed metrics displayed]

============================================================
Test completed successfully!
============================================================
```

### 3. Web Interface (Streamlit)

Launch the interactive demo:

```bash
streamlit run app.py
```

The browser will open automatically to `http://localhost:8501`.

#### Using the Web Interface

1. **Upload an Image**
   - Click "Browse files" to upload a grayscale image
   - Supported formats: PNG, JPG, JPEG, BMP, TIFF
   - Non-grayscale images will be automatically converted

2. **Generate Keys & Encrypt**
   - Click "Generate Quantum Keys & Encrypt"
   - Quantum keys are generated using Qiskit
   - Image is encrypted using XOR and permutation
   - View the encrypted image

3. **Decrypt**
   - Click "Decrypt Image"
   - Image is decrypted using the same keys
   - View the decrypted image
   - Check PSNR to verify perfect reconstruction

4. **Analyze Results**
   - View entropy, uniformity, and correlation metrics
   - Compare histograms (original vs. encrypted)
   - Examine correlation plots
   - Review detailed metrics table

### 4. Python API Usage

#### Basic Encryption/Decryption

```python
from quantum_key_generator import generate_quantum_key
from image_encryptor import ImageEncryptor, load_image_as_grayscale, save_image_array

# Load image
original = load_image_as_grayscale('path/to/image.png')

# Generate quantum keys
keystream, permutation_seed = generate_quantum_key(original.size)

# Encrypt
encryptor = ImageEncryptor(keystream, permutation_seed)
encrypted = encryptor.encrypt_image(original)

# Save encrypted image
save_image_array(encrypted, 'encrypted.png')

# Decrypt
decrypted = encryptor.decrypt_image(encrypted)

# Save decrypted image
save_image_array(decrypted, 'decrypted.png')
```

#### Image Analysis

```python
from image_analysis import analyze_image, calculate_psnr

# Analyze original image
original_metrics = analyze_image(original)
print(f"Original Entropy: {original_metrics['entropy']:.4f} bits")

# Analyze encrypted image
encrypted_metrics = analyze_image(encrypted)
print(f"Encrypted Entropy: {encrypted_metrics['entropy']:.4f} bits")

# Verify decryption quality
psnr = calculate_psnr(original, decrypted)
print(f"PSNR: {psnr} dB")
```

#### Generate Visualizations

```python
from image_analysis import generate_histogram_plot, generate_correlation_plot

# Generate histogram
hist_bytes = generate_histogram_plot(encrypted, "Encrypted Histogram")
with open('histogram.png', 'wb') as f:
    f.write(hist_bytes)

# Generate correlation plot
corr_bytes = generate_correlation_plot(encrypted, 'horizontal', "Correlation")
with open('correlation.png', 'wb') as f:
    f.write(corr_bytes)
```

## Understanding the Metrics

### Entropy
- **Range**: 0 to 8 bits (for 8-bit grayscale images)
- **Good encryption**: Close to 8 bits
- **Meaning**: Higher entropy = more randomness = better security

### Histogram Uniformity
- **Range**: 0 to 1
- **Good encryption**: Close to 1
- **Meaning**: Uniform distribution = harder to detect patterns

### Correlation Coefficient
- **Range**: -1 to 1
- **Good encryption**: Close to 0
- **Meaning**: Low correlation = adjacent pixels are independent

### PSNR (Peak Signal-to-Noise Ratio)
- **Range**: 0 to ∞ dB
- **Perfect decryption**: ∞ dB
- **Meaning**: Measures quality of decrypted image vs. original

## Advanced Options

### Using a Seed for Reproducibility

In the web interface:
1. Check "Use seed for reproducibility" in the sidebar
2. Enter a seed value (e.g., 42)

In Python:
```python
keystream, permutation_seed = generate_quantum_key(image_size, seed=42)
```

**Note**: Using a seed makes the quantum randomness deterministic (useful for testing but not recommended for production).

### Working with Different Image Sizes

The system automatically adapts to any image size:

```python
# Small image (64x64)
small_image = load_image_as_grayscale('small.png')  # 4096 pixels
keystream, seed = generate_quantum_key(small_image.size)

# Large image (512x512)
large_image = load_image_as_grayscale('large.png')  # 262144 pixels
keystream, seed = generate_quantum_key(large_image.size)
```

**Note**: Larger images require more quantum key generation time.

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Streamlit not opening
```bash
# Try specifying the port
streamlit run app.py --server.port 8501
```

### Quantum circuit generation is slow
- This is normal for large images
- The system uses multiple shots per circuit for efficiency
- Consider using smaller images for testing

### Out of memory errors
- Reduce image size
- Close other applications
- Increase system memory

## Tips for Best Results

1. **Image Format**: Use grayscale images for best results
2. **Image Size**: Start with 256x256 or smaller for faster processing
3. **Seed Usage**: Only use seeds for testing/debugging, not production
4. **Key Storage**: In production, securely store and transmit keys separately
5. **Analysis**: Always verify PSNR = ∞ to ensure perfect decryption

## Next Steps

- Experiment with different images
- Compare metrics across various image types
- Explore the correlation between image complexity and encryption quality
- Try implementing additional encryption layers
- Integrate with other quantum algorithms

For more information, see the main [README.md](README.md).
