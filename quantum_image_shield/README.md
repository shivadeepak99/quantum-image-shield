# 🔮 Quantum-Seed ImageShield - v2.0.0

> Enterprise-grade hybrid quantum-classical image encryption powered by IBM Qiskit

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.2-purple.svg)](https://qiskit.org/)
[![Go Backend](https://img.shields.io/badge/Backend-Golang-00ADD8.svg)](https://go.dev/)

##  🌟 Overview

**Quantum-Seed ImageShield** is a production-ready image encryption system that combines **quantum-generated randomness** from IBM Qiskit with classical encryption techniques to create an enterprise-grade security solution.

### ✨ Key Features

- ⚛️ **True Quantum Randomness** - Hadamard gates + quantum measurements  
- 🔒 **Hybrid Encryption** - XOR cipher + quantum permutation  
- 🎯 **3 Purity Levels** - Maximum, Balanced (recommended), Fast  
- 🛡️ **Enterprise Security** - PBKDF2, HMAC, encrypted key storage  
- 🚀 **Lossless** - Perfect reconstruction (PSNR = ∞)  
- 📊 **Analytics Ready** - Entropy, correlation, PSNR metrics  

## 🚀 Quick Start

### Installation

```powershell
# Clone repository
git clone <repository-url>
cd quantum-image-shield

# Create virtual environment
python -m venv venv
.\\venv\\Scripts\\Activate.ps1

# Install dependencies
pip install -r quantum_image_shield/requirements.txt
```

### Usage

#### Encrypt
```powershell
python -m quantum_image_shield.cli encrypt input.png encrypted.png --purity balanced
```

#### Decrypt
```powershell
python -m quantum_image_shield.cli decrypt encrypted.png decrypted.png --key encrypted_keys.npz
```

## 🎯 Quantum Purity Levels

| Level | Speed | Security | Use Case |
|-------|-------|----------|----------|
| **maximum** | 🐌 Slow | 🛡️🛡️🛡️ | Government, medical |
| **balanced** | ⚡ Fast | 🛡️🛡️ | ✅ Production (recommended) |
| **fast** | 🚀 Instant | 🛡️ | Development |

## 📦 What's New in v2.0

✅ **Phase 1 Complete:**
- Fixed quantum permutation bug (true quantum randomness)
- Added cryptographic hardening (PBKDF2, HMAC)
- Comprehensive input validation
- Enterprise-grade error handling
- Unit test suite

## 🗺️ Roadmap

- ✅ **Phase 1**: Core Python engine with security (COMPLETE)
- 🚧 **Phase 2**: Golang API backend with gRPC
- 📅 **Phase 3**: Analytics & metrics module
- 📅 **Phase 4**: Next.js frontend
- 📅 **Phase 5**: Production deployment

See [ENTERPRISE_ARCHITECTURE_PLAN.md](ENTERPRISE_ARCHITECTURE_PLAN.md) for full details.

## 📖 Documentation

Full architecture and implementation plan available in:
- [ENTERPRISE_ARCHITECTURE_PLAN.md](ENTERPRISE_ARCHITECTURE_PLAN.md)

---

**Built with 💜** | *True quantum randomness meets classical security* ⚛️🔐
