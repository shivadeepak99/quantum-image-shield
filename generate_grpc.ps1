# 🔧 Generate gRPC stubs (PowerShell version)

Write-Host "🔮 Generating gRPC stubs from quantum.proto..." -ForegroundColor Cyan

# Python stubs
Write-Host "`n📦 Generating Python stubs..." -ForegroundColor Yellow
python -m grpc_tools.protoc `
    -I./backend/pkg/grpc `
    --python_out=. `
    --grpc_python_out=. `
    backend/pkg/grpc/quantum.proto

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python stubs generated!" -ForegroundColor Green
} else {
    Write-Host "❌ Python stub generation failed!" -ForegroundColor Red
    Write-Host "   Install with: pip install grpcio-tools" -ForegroundColor Yellow
    exit 1
}

# Go stubs (requires protoc-gen-go and protoc-gen-go-grpc)
Write-Host "`n📦 Generating Go stubs..." -ForegroundColor Yellow
protoc `
    -I./backend/pkg/grpc `
    --go_out=./backend/pkg/grpc `
    --go_opt=paths=source_relative `
    --go-grpc_out=./backend/pkg/grpc `
    --go-grpc_opt=paths=source_relative `
    backend/pkg/grpc/quantum.proto

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Go stubs generated!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Go stub generation failed (protoc not found)" -ForegroundColor Yellow
    Write-Host "   Install protoc: https://grpc.io/docs/protoc-installation/" -ForegroundColor Gray
    Write-Host "   Install go plugins:" -ForegroundColor Gray
    Write-Host "     go install google.golang.org/protobuf/cmd/protoc-gen-go@latest" -ForegroundColor Gray
    Write-Host "     go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest" -ForegroundColor Gray
}

Write-Host "`n🎯 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Install grpcio: pip install -r requirements-grpc.txt" -ForegroundColor White
Write-Host "   2. Start Python server: python python_grpc_server.py" -ForegroundColor White
Write-Host "   3. Start Go API: cd backend; go run cmd/api/main.go" -ForegroundColor White
