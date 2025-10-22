# 🚀 SIMPLE MVP - No Docker, No DB, No Redis!

Quick prototype setup for quantum image encryption.

## 🎯 What This Does

**Go Backend** → calls → **Python CLI** → **Quantum Encryption**

Super simple! No databases, no message queues, just pure quantum power!

## 🏃 Quick Start

### 1. Start Go API

```powershell
cd backend
go run cmd/api/main.go
```

Server runs on: http://localhost:8080

### 2. Test Encryption

```powershell
curl -X POST http://localhost:8080/api/v1/encrypt `
  -F "image=@../samples/sample_image.png" `
  -F "purity=balanced"
```

### 3. Test Decryption

```powershell
# Use the paths from encryption response
curl -X POST http://localhost:8080/api/v1/decrypt `
  -F "encrypted_image=@C:/Temp/quantum-jobs/{job_id}/encrypted.png" `
  -F "key_file=@C:/Temp/quantum-jobs/{job_id}/encrypted_keys.npz"
```

## 📁 How It Works

```
Upload Image → Go API → Python subprocess → Quantum Core
                ↓
         Save to /tmp/quantum-jobs/{uuid}/
                ↓
         Return file paths
```

No persistence! Files stay in temp folder for download.

## 🎨 Next: Frontend

Coming next - drag & drop React/Next.js UI!

---

Built with 💜 by your quantum waifu
