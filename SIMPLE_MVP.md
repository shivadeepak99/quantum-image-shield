# 🚀 QUANTUM IMAGESHIELD - SIMPLE MVP

**Pure prototype: Next.js frontend → Go backend → Python quantum core**

No database, no Redis, no Docker. Just quantum magic! ✨

---

## 🏗️ Architecture

```
┌──────────────────┐
│  Next.js 14 UI   │  Port 3000
│  (React + TS)    │
└────────┬─────────┘
         │ HTTP
         ▼
┌──────────────────┐
│   Go Fiber API   │  Port 8080
│   (Lightweight)  │
└────────┬─────────┘
         │ exec.Command()
         ▼
┌──────────────────┐
│  Python CLI      │
│  Quantum Core    │
└──────────────────┘
```

---

## 🚀 Quick Start

### **1. Start Go Backend**

```powershell
cd backend
go run cmd/api/main.go
```

Server: http://localhost:8080

### **2. Start Next.js Frontend**

```powershell
cd frontend
npm install
npm run dev
```

UI: http://localhost:3000

### **3. Use the App!**

1. Drag & drop an image
2. Choose purity level (fast/balanced/maximum)
3. Click "Encrypt"
4. Download encrypted image + key file
5. Upload both to decrypt!

---

## 📁 File Structure

```
quantum-image-shield/
├── frontend/              # Next.js 14 + TypeScript + Tailwind
│   ├── src/app/
│   │   ├── page.tsx      # Main UI (drag-drop, encrypt/decrypt)
│   │   ├── layout.tsx
│   │   └── globals.css
│   └── package.json
│
├── backend/               # Go Fiber API
│   └── cmd/api/main.go   # Simple REST endpoints
│
└── quantum_image_shield/  # Python quantum core
    ├── encryption.py
    └── cli.py
```

---

## 🎨 Features

✅ **Drag & drop image upload**  
✅ **3 quantum purity levels**  
✅ **Real-time encryption progress**  
✅ **Dark mode UI (purple/pink gradient)**  
✅ **Encrypt + Decrypt modes**  
✅ **File download results**  

---

## 🔧 How It Works

### **Encryption Flow:**
1. User uploads image in Next.js UI
2. Frontend sends FormData to `localhost:8080/api/v1/encrypt`
3. Go API saves file to temp folder
4. Go calls: `python -m quantum_image_shield.cli encrypt ...`
5. Python returns encrypted image + keys
6. Go returns file paths to frontend
7. User downloads files

### **Decryption Flow:**
1. User uploads encrypted image + key file
2. Frontend sends to `localhost:8080/api/v1/decrypt`
3. Go API calls Python CLI
4. Returns decrypted image
5. Perfect lossless recovery! ✨

---

## 🎯 API Endpoints

### **POST /api/v1/encrypt**
```
FormData:
  - image: file
  - purity: "fast" | "balanced" | "maximum"

Response:
{
  "success": true,
  "job_id": "uuid",
  "output_path": "/tmp/quantum-jobs/{uuid}/encrypted.png",
  "key_path": "/tmp/quantum-jobs/{uuid}/encrypted_keys.npz",
  "purity": "balanced"
}
```

### **POST /api/v1/decrypt**
```
FormData:
  - encrypted_image: file
  - key_file: file (.npz)

Response:
{
  "success": true,
  "job_id": "uuid",
  "output_path": "/tmp/quantum-jobs/{uuid}/decrypted.png"
}
```

---

## 💜 What's Next?

**Phase 3 - Add bells & whistles:**
- Image preview (before/after)
- Progress bar with WebSockets
- Batch processing
- Download buttons (instead of file paths)
- Encryption analytics (entropy, pixel change %)

**Phase 4 - Production features:**
- User authentication (JWT)
- Job history (PostgreSQL)
- Cloud storage (AWS S3)
- Payment system (Stripe)

---

## 🐛 Troubleshooting

**"Go: command not found"**
```powershell
# Install Go: https://go.dev/dl/
# Or: winget install GoLang.Go
```

**"Cannot connect to backend"**
```powershell
# Make sure Go server is running on port 8080
cd backend
go run cmd/api/main.go
```

**"Python encryption failed"**
```powershell
# Make sure quantum package is installed
pip install -e .
```

---

Built with 💜 by your quantum dev waifu
