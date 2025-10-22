# 🚀 Quantum ImageShield - Golang Backend API

High-performance REST API backend for quantum image encryption, built with Go + Fiber.

## 🏗️ Architecture

```
backend/
├── cmd/
│   └── api/              # Main application entry point
│       └── main.go
├── internal/             # Private application code
│   ├── handlers/         # HTTP request handlers
│   ├── services/         # Business logic layer
│   ├── models/           # Database models (GORM)
│   └── middleware/       # Auth, CORS, logging, etc.
├── pkg/                  # Public libraries
│   └── grpc/             # gRPC client to Python quantum service
├── config/               # Configuration files
└── go.mod                # Go module dependencies
```

## 🔥 Tech Stack

- **Framework:** Fiber v2 (Express-like, blazing fast)
- **Database:** PostgreSQL (GORM ORM)
- **Cache/Queue:** Redis (job queues, sessions)
- **Auth:** JWT tokens
- **IPC:** gRPC to Python quantum core
- **Logging:** Zerolog
- **Config:** godotenv + environment variables

## 🚀 Quick Start

```bash
# Navigate to backend
cd backend

# Install dependencies
go mod download

# Set up environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations (coming soon)
# go run cmd/migrate/main.go

# Start development server
go run cmd/api/main.go
```

Server runs on: http://localhost:8080

## 📡 API Endpoints

### **Encryption**
```http
POST /api/v1/encrypt
Content-Type: multipart/form-data

{
  "image": <file>,
  "purity": "balanced" | "maximum" | "fast",
  "password": "optional"
}

Response: {
  "job_id": "uuid",
  "status": "queued"
}
```

### **Decryption**
```http
POST /api/v1/decrypt
Content-Type: multipart/form-data

{
  "encrypted_image": <file>,
  "key_file": <file>
}

Response: {
  "job_id": "uuid",
  "status": "queued"
}
```

### **Job Status**
```http
GET /api/v1/jobs/:job_id

Response: {
  "job_id": "uuid",
  "status": "processing" | "completed" | "failed",
  "progress": 75,
  "result_url": "https://...",
  "error": null
}
```

### **WebSocket Progress**
```javascript
ws://localhost:8080/ws/jobs/:job_id

Message: {
  "progress": 50,
  "status": "encrypting",
  "message": "Generating quantum keys..."
}
```

## 🔐 Authentication

JWT-based authentication with refresh tokens.

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
```

Protected routes require header:
```
Authorization: Bearer <jwt_token>
```

## 🐳 Docker

```bash
# Build image
docker build -t quantum-api:latest .

# Run container
docker run -p 8080:8080 --env-file .env quantum-api:latest
```

## 🧪 Testing

```bash
# Run unit tests
go test ./...

# Run with coverage
go test -cover ./...

# Integration tests
go test -tags=integration ./...
```

## 📊 Performance Targets

- Latency: <100ms (API response time)
- Throughput: 1000 req/sec (with load balancing)
- Concurrency: 10,000 goroutines
- Memory: <512MB idle, <2GB under load

## 🛠️ Development

```bash
# Install dev tools
go install github.com/cosmtrek/air@latest  # Hot reload
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest  # Linter

# Run with hot reload
air

# Lint code
golangci-lint run
```

## 📝 TODO

- [ ] Implement all API endpoints
- [ ] Add database migrations
- [ ] Set up Redis job queue
- [ ] Create gRPC client to Python service
- [ ] Add comprehensive tests
- [ ] Swagger/OpenAPI documentation
- [ ] Rate limiting & API throttling
- [ ] Metrics & monitoring (Prometheus)

---

Built with 💜 by your quantum dev waifu
