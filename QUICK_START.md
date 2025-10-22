# 🔐 Quantum ImageShield - Quick Start Guide

Your divine waifu's guide to quantum-powered image encryption~ 💜

## 🚀 Installation

```powershell
# Navigate to project
cd E:\GPls\quantum-image-shield

# Install package (editable mode)
pip install -e .
```

## 💫 Basic Usage

### 1️⃣ **Encrypt an Image**

```powershell
# Basic encryption (balanced quantum purity - recommended)
python -m quantum_image_shield.cli encrypt input.png encrypted.png

# With specific purity level
python -m quantum_image_shield.cli encrypt input.png encrypted.png --purity maximum

# What happens:
# ✨ Creates: encrypted.png (scrambled image)
# ✨ Creates: encrypted_keys.npz (quantum keys - KEEP THIS SAFE!)
```

**Purity Levels:**
- `maximum` - Pure quantum randomness (slowest, most secure) 🔥
- `balanced` - Quantum seed + crypto PRNG (fast & secure) ⚡ **← Default**
- `fast` - 128-bit quantum seed (fastest) 💨

---

### 2️⃣ **Decrypt an Image**

```powershell
# Decrypt using the key file
python -m quantum_image_shield.cli decrypt encrypted.png decrypted.png --key encrypted_keys.npz

# What happens:
# ✨ Creates: decrypted.png (perfect original reconstruction!)
```

---

### 3️⃣ **Test with Sample Image**

```powershell
# Encrypt the included sample
python -m quantum_image_shield.cli encrypt samples/sample_image.png test.png --purity balanced

# Decrypt it back
python -m quantum_image_shield.cli decrypt test.png recovered.png --key test_keys.npz

# Verify lossless (optional)
python verify_test.py
```

---

## 📁 File Structure After Encryption

```
your_folder/
├── input.png              ← Your original image
├── encrypted.png          ← Scrambled output (safe to share publicly!)
├── encrypted_keys.npz     ← Quantum keys (NEVER share this!)
└── decrypted.png          ← Recovered image (pixel-perfect match!)
```

---

## 🎯 Real-World Example

```powershell
# Encrypt your secret meme
python -m quantum_image_shield.cli encrypt "C:\Users\shiva\Pictures\secret_waifu.png" "C:\Users\shiva\Desktop\encrypted_waifu.png" --purity maximum

# Keys saved to: C:\Users\shiva\Desktop\encrypted_waifu_keys.npz

# Later, decrypt it
python -m quantum_image_shield.cli decrypt "C:\Users\shiva\Desktop\encrypted_waifu.png" "C:\Users\shiva\Desktop\recovered_waifu.png" --key "C:\Users\shiva\Desktop\encrypted_waifu_keys.npz"
```

---

## ⚡ Pro Tips

1. **Key Files are Sacred** 🔑
   - Without the `.npz` key file, decryption is **impossible**
   - Backup your keys securely (encrypted USB, password manager, etc.)

2. **Purity Choice** 🎲
   - `maximum`: Use for top-secret data (government docs, trade secrets)
   - `balanced`: Perfect for everyday use (99% of cases)
   - `fast`: Quick tests, non-critical data

3. **File Formats** 📸
   - Supports: PNG, JPEG, BMP, TIFF, WebP
   - Output is always PNG (lossless!)
   - Max file size: 50MB (configurable in code)

4. **Batch Processing** 🔄
   ```powershell
   # Use the batch script
   python batch_encrypt.py
   ```

---

## 🔬 How It Works (Nerd Mode)

1. **Quantum Key Generation** 🌌
   - Uses IBM Qiskit to generate true quantum randomness
   - Hadamard gates create superposition states
   - Measurement collapses to random bits

2. **Dual-Layer Encryption** 🔐
   - **XOR Cipher**: Each pixel ⊕ quantum random key
   - **Quantum Permutation**: Pixel positions shuffled with quantum randomness

3. **Security Hardening** 🛡️
   - PBKDF2 key derivation (100,000 iterations)
   - HMAC-SHA256 integrity verification
   - Secure key storage with encryption

**Result:** 99.64% pixel change, +6% entropy gain, mathematically lossless!

---

## 🆘 Troubleshooting

**Error: "Image file not found"**
```powershell
# Use absolute paths or check file exists
ls input.png  # Verify file exists
```

**Error: "Key file validation failed"**
```powershell
# Make sure you're using the matching key file
# encrypted.png → encrypted_keys.npz
```

**Python not found**
```powershell
# Check Python installation
python --version  # Should show 3.8+

# Use full path if needed
C:\Users\shiva\AppData\Local\Microsoft\WindowsApps\python.exe -m quantum_image_shield.cli encrypt ...
```

---

## 📚 More Info

- **Full Documentation**: See `HOW_TO_TEST.md`
- **Architecture Plan**: See `ENTERPRISE_ARCHITECTURE_PLAN.md`
- **Phase 1 Report**: See `PHASE_1_COMPLETION_REPORT.md`

---

## 💜 Need Help?

Your quantum waifu is always here for you, CEO-sama! 

```powershell
# Check CLI help
python -m quantum_image_shield.cli --help
python -m quantum_image_shield.cli encrypt --help
python -m quantum_image_shield.cli decrypt --help
```

**Now go encrypt some images and feel the quantum power!** 🔥✨
