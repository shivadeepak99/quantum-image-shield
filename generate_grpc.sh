#!/bin/bash
# 🔧 Generate gRPC stubs for Python and Go

echo "🔮 Generating gRPC stubs from quantum.proto..."

# Python stubs
echo "📦 Generating Python stubs..."
python -m grpc_tools.protoc \
    -I./backend/pkg/grpc \
    --python_out=. \
    --grpc_python_out=. \
    backend/pkg/grpc/quantum.proto

echo "✅ Python stubs generated!"

# Go stubs (requires protoc-gen-go and protoc-gen-go-grpc)
echo "📦 Generating Go stubs..."
protoc \
    -I./backend/pkg/grpc \
    --go_out=./backend/pkg/grpc \
    --go_opt=paths=source_relative \
    --go-grpc_out=./backend/pkg/grpc \
    --go-grpc_opt=paths=source_relative \
    backend/pkg/grpc/quantum.proto

echo "✅ Go stubs generated!"
echo ""
echo "🎯 Next steps:"
echo "   1. Install grpcio: pip install -r requirements-grpc.txt"
echo "   2. Start Python server: python python_grpc_server.py"
echo "   3. Start Go API: cd backend && go run cmd/api/main.go"
