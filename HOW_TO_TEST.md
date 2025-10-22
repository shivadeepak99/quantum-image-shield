# 🎨 **QUICK START GUIDE - Test Your Own Images**

Welcome, CEO-sama! Here's how to test Quantum-Seed ImageShield with your own images! 💜

---

## 📍 **Step 1: Get to the Right Folder**

```powershell
cd E:\GPls\quantum-image-shield
```

---

## 🖼️ **Step 2: Choose Your Method**

### **Method A: Direct Path (Easiest)**

Encrypt any image on your computer:

```powershell
# Replace with YOUR image path
python -m quantum_image_shield.cli encrypt "C:\Users\YourName\Pictures\photo.jpg" encrypted.png

# Decrypt it back
python -m quantum_image_shield.cli decrypt encrypted.png decrypted.png --key encrypted_keys.npz
```

**Examples:**
```powershell
# Desktop image
python -m quantum_image_shield.cli encrypt "C:\Users\shiva\Desktop\myimage.png" output.png

# Downloads folder
python -m quantum_image_shield.cli encrypt "C:\Users\shiva\Downloads\photo.jpg" secure.png

# Use fast mode for quick testing
python -m quantum_image_shield.cli encrypt "C:\path\to\image.jpg" test.png --purity fast
```

---

### **Method B: Copy Image to Project (Simple)**

1. **Copy your image** to `E:\GPls\quantum-image-shield\`
2. **Run the command** (no long paths needed!):

```powershell
# If your image is named "vacation.jpg"
python -m quantum_image_shield.cli encrypt vacation.jpg encrypted_vacation.png

# Decrypt
python -m quantum_image_shield.cli decrypt encrypted_vacation.png decrypted_vacation.png --key encrypted_vacation_keys.npz
```

---

### **Method C: Batch Test Multiple Images**

Test ALL images in a folder at once:

```powershell
# Test a single image
python batch_encrypt.py myimage.png

# Test all images in a folder
python batch_encrypt.py "C:\Users\shiva\Pictures"

# Test samples folder
python batch_encrypt.py samples

# Use maximum security mode
python batch_encrypt.py myimage.png maximum
```

This will:
- ✅ Validate each image
- ✅ Encrypt with quantum randomness
- ✅ Decrypt and verify lossless
- ✅ Show entropy improvement
- ✅ Calculate statistics

---

## 🎯 **Purity Levels Explained**

| Flag | Speed | Security | When to Use |
|------|-------|----------|-------------|
| `--purity fast` | 🚀 Instant | Good | Quick tests, development |
| `--purity balanced` | ⚡ ~1 sec | High | ✅ **Default - Use this!** |
| `--purity maximum` | 🐌 5-15 min | Maximum | Ultra-secure, small images |

---

## 📋 **Full Command Reference**

### **Encryption**
```powershell
python -m quantum_image_shield.cli encrypt INPUT OUTPUT [OPTIONS]

OPTIONS:
  --purity {fast|balanced|maximum}  # Quantum randomness level (default: balanced)
  --key PATH                        # Custom key file path (auto-generated if omitted)
  --seed NUMBER                     # For reproducible testing only
```

### **Decryption**
```powershell
python -m quantum_image_shield.cli decrypt ENCRYPTED OUTPUT --key KEYFILE
```

---

## 🎨 **Try These Examples NOW!**

### **Example 1: Quick Test**
```powershell
python -m quantum_image_shield.cli encrypt samples/sample_image.png my_test.png --purity fast
python -m quantum_image_shield.cli decrypt my_test.png recovered.png --key my_test_keys.npz
```

### **Example 2: Your Desktop Photo**
```powershell
python -m quantum_image_shield.cli encrypt "C:\Users\shiva\Desktop\photo.jpg" secure_photo.png --purity balanced
```

### **Example 3: Batch Test Your Pictures Folder**
```powershell
python batch_encrypt.py "C:\Users\shiva\Pictures"
```

---

## 🔍 **Verify Results**

After encryption/decryption, check your files:

```powershell
# List generated files
ls *.png, *.npz | Select-Object Name, Length

# Visual check - open in image viewer
explorer decrypted.png
```

---

## 💡 **Pro Tips**

1. **Supported Formats**: PNG, JPEG, JPG, BMP, TIFF, WEBP
2. **Size Limits**: Max 50 MB file size, 25 megapixels
3. **Key Storage**: NEVER lose your `*_keys.npz` file - you can't decrypt without it!
4. **Output Format**: Always saves as PNG (lossless)
5. **Speed**: 
   - Small images (< 1 MB): < 1 second
   - Large images (5 MB): 2-3 seconds
   - Maximum purity: Much slower (use for final production only)

---

## 🆘 **Troubleshooting**

### **"File not found"**
```powershell
# Use absolute path with quotes
python -m quantum_image_shield.cli encrypt "C:\Full\Path\To\image.jpg" output.png
```

### **"Invalid image file"**
- Check file isn't corrupted
- Ensure it's a real image (not renamed .txt)
- Try opening in Paint/Photoshop first

### **"File too large"**
- Resize your image (max 50 MB)
- Or use `maximum` purity for better compression

---

## 🎉 **You're Ready!**

Just run:
```powershell
python -m quantum_image_shield.cli encrypt YOUR_IMAGE.jpg encrypted.png --purity balanced
```

That's it! Your image is now secured with **quantum randomness**! 🔮✨

---

**Happy encrypting, CEO-sama!** 💜

Questions? Just ask your dev waifu~ 😘
