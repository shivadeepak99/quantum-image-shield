# 🚀 Quantum ImageShield - Development Guide

Complete setup guide for Phase 2 Golang backend + Python gRPC service.

---

## 📋 Prerequisites

### Required
- **Go 1.21+**: [Download](https://go.dev/dl/)
- **Python 3.11+**: Already installed ✅
- **Docker & Docker Compose**: [Download](https://www.docker.com/products/docker-desktop/)

### Optional (for local dev without Docker)
- **PostgreSQL 16**: [Download](https://www.postgresql.org/download/)
- **Redis 7**: [Download](https://redis.io/download/)
- **protoc compiler**: [Install guide](https://grpc.io/docs/protoc-installation/)

---

## 🏗️ Setup Instructions

### **1. Install Go Dependencies**

```powershell
cd backend
go mod download
```

### **2. Install Python gRPC Tools**

```powershell
pip install -r requirements-grpc.txt
```

### **3. Generate gRPC Stubs**

```powershell
# From project root
.\generate_grpc.ps1
```

This creates:
- `quantum_pb2.py` & `quantum_pb2_grpc.py` (Python)
- `quantum.pb.go` & `quantum_grpc.pb.go` (Go)

### **4. Configure Environment**

```powershell
cd backend
cp .env.example .env
# Edit .env with your settings
```

---

## 🐳 Docker Setup (Recommended)

### **Start All Services**

```powershell
# Production mode
docker-compose up -d

# Development mode (includes pgAdmin, Redis Commander)
docker-compose --profile dev up -d
```

### **Services Running:**
- **API**: http://localhost:8080
- **Python gRPC**: localhost:50051
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **pgAdmin** (dev): http://localhost:5050
- **Redis Commander** (dev): http://localhost:8081

### **Check Status**

```powershell
docker-compose ps
docker-compose logs -f api
docker-compose logs -f quantum-service
```

### **Stop Services**

```powershell
docker-compose down
# Or with volume cleanup:
docker-compose down -v
```

---

## 💻 Local Development (Without Docker)

### **1. Start PostgreSQL & Redis**

```powershell
# Install via Chocolatey (Windows)
choco install postgresql redis

# Start services
Start-Service postgresql-x64-16
Start-Service redis
```

### **2. Start Python gRPC Server**

```powershell
python python_grpc_server.py
# Runs on port 50051
```

### **3. Start Go API Server**

```powershell
cd backend
go run cmd/api/main.go
# Runs on port 8080
```

---

## 🧪 Testing the API

### **Health Check**

```powershell
curl http://localhost:8080/health
```

### **Encrypt Image** (once implemented)

```powershell
curl -X POST http://localhost:8080/api/v1/encrypt `
  -F "image=@samples/sample_image.png" `
  -F "purity=balanced"
```

### **Get Job Status**

```powershell
curl http://localhost:8080/api/v1/jobs/{job_id}
```

---

## 📁 Project Structure

```
quantum-image-shield/
├── backend/                    # Go API server
│   ├── cmd/api/               # Main entry point
│   ├── internal/              # Private application code
│   │   ├── handlers/          # HTTP handlers
│   │   ├── services/          # Business logic
│   │   ├── models/            # Database models
│   │   └── middleware/        # Auth, CORS, etc.
│   ├── pkg/grpc/              # gRPC client & proto
│   └── Dockerfile
├── quantum_image_shield/       # Python quantum core
├── python_grpc_server.py      # Python gRPC service
├── docker-compose.yml         # Container orchestration
└── generate_grpc.ps1          # Protobuf generation
```

---

## 🔧 Development Workflow

### **Hot Reload (Go)**

```powershell
# Install Air
go install github.com/cosmtrek/air@latest

# Run with hot reload
cd backend
air
```

### **Rebuild Docker Images**

```powershell
docker-compose build --no-cache
docker-compose up -d
```

### **Run Tests**

```powershell
# Go tests
cd backend
go test ./...

# Python tests
pytest quantum_image_shield/tests/
```

---

## 🐛 Troubleshooting

### **"go: command not found"**
Add Go to PATH:
```powershell
$env:Path += ";C:\Program Files\Go\bin"
```

### **"protoc: command not found"**
Install Protocol Buffer Compiler:
```powershell
choco install protoc
# Or download from: https://github.com/protocolbuffers/protobuf/releases
```

### **Docker port already in use**
```powershell
# Check what's using port 8080
netstat -ano | findstr :8080
# Kill the process or change port in docker-compose.yml
```

### **Database connection failed**
```powershell
# Check PostgreSQL is running
docker-compose logs postgres
# Verify credentials in .env match docker-compose.yml
```

---

## 📚 Next Steps

1. ✅ **Setup complete!** - All services running
2. 🔄 **Implement endpoints** - POST /encrypt, POST /decrypt
3. 🔐 **Add JWT auth** - User registration/login
4. 📊 **Add monitoring** - Prometheus + Grafana
5. 🚀 **Deploy to cloud** - AWS/Azure/GCP

---

## 💜 Support

Created with love by your quantum dev waifu~ ✨

Issues? Check:
- `backend/README.md` - API documentation
- `ENTERPRISE_ARCHITECTURE_PLAN.md` - Full roadmap
- `HOW_TO_TEST.md` - Testing guide
