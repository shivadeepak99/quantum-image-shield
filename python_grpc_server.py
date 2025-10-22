#!/usr/bin/env python3
"""
🔮 Quantum Encryption gRPC Server
Python service that exposes quantum encryption via gRPC to Go API
"""

import grpc
from concurrent import futures
import time
import io
import numpy as np
from PIL import Image

# Import our quantum core
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from quantum_image_shield.encryption import ImageEncryption

# Import generated protobuf (will be generated)
# import quantum_pb2
# import quantum_pb2_grpc

class QuantumEncryptionServicer:
    """💜 gRPC service implementation"""
    
    def __init__(self):
        print("🔮 Quantum service initialized!")
    
    def EncryptImage(self, request, context):
        """Encrypt an image with quantum randomness"""
        try:
            print(f"📥 Received encryption request (purity: {request.purity_level})")
            
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(request.image_data))
            
            # Create encryptor
            encryptor = ImageEncryption(quantum_purity=request.purity_level or 'balanced')
            
            # Encrypt to bytes (not file)
            encrypted_array, keys = encryptor.encrypt_array(np.array(image))
            
            # Convert encrypted array back to image bytes
            encrypted_image = Image.fromarray(encrypted_array.astype('uint8'))
            encrypted_bytes = io.BytesIO()
            encrypted_image.save(encrypted_bytes, format='PNG')
            
            # Serialize keys to bytes
            key_bytes = io.BytesIO()
            np.savez_compressed(key_bytes, 
                               xor_key=keys['xor_key'], 
                               permutation=keys['permutation'])
            
            # Calculate metrics
            orig_entropy = _calculate_entropy(np.array(image))
            enc_entropy = _calculate_entropy(encrypted_array)
            pixel_change = np.sum(np.array(image) != encrypted_array) / np.array(image).size * 100
            
            # Build response (TODO: Use actual protobuf)
            print(f"✅ Encryption complete! {pixel_change:.2f}% changed")
            
            # Return dict for now (will be protobuf response)
            return {
                'encrypted_image': encrypted_bytes.getvalue(),
                'key_data': key_bytes.getvalue(),
                'metadata': {
                    'xor_key_length': len(keys['xor_key']),
                    'permutation_size': len(keys['permutation']),
                    'purity_level': request.purity_level or 'balanced',
                    'original_width': image.width,
                    'original_height': image.height,
                    'entropy_original': orig_entropy,
                    'entropy_encrypted': enc_entropy,
                    'pixel_change_rate': pixel_change,
                }
            }
            
        except Exception as e:
            print(f"❌ Encryption failed: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Encryption error: {str(e)}")
            return None
    
    def DecryptImage(self, request, context):
        """Decrypt an encrypted image"""
        try:
            print("📥 Received decryption request")
            
            # Load encrypted image
            encrypted_image = Image.open(io.BytesIO(request.encrypted_image))
            
            # Load keys from bytes
            key_file = io.BytesIO(request.key_data)
            keys = np.load(key_file, allow_pickle=False)
            
            # Decrypt
            encryptor = ImageEncryption()
            decrypted_array = encryptor.decrypt_array(
                np.array(encrypted_image),
                keys['xor_key'],
                keys['permutation']
            )
            
            # Convert to bytes
            decrypted_image = Image.fromarray(decrypted_array.astype('uint8'))
            decrypted_bytes = io.BytesIO()
            decrypted_image.save(decrypted_bytes, format='PNG')
            
            print("✅ Decryption complete!")
            
            return {
                'decrypted_image': decrypted_bytes.getvalue(),
                'metadata': {
                    'width': decrypted_image.width,
                    'height': decrypted_image.height,
                    'format': 'PNG',
                    'lossless': True,
                }
            }
            
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Decryption error: {str(e)}")
            return None
    
    def Ping(self, request, context):
        """Health check"""
        return {
            'message': f"Pong! {request.message}",
            'version': '2.0.0',
            'quantum_ready': True,
        }


def _calculate_entropy(img_array):
    """Calculate Shannon entropy"""
    values, counts = np.unique(img_array, return_counts=True)
    probabilities = counts / img_array.size
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
    return entropy


def serve():
    """Start gRPC server"""
    # TODO: Use actual protobuf after generation
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # quantum_pb2_grpc.add_QuantumEncryptionServiceServicer_to_server(
    #     QuantumEncryptionServicer(), server
    # )
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ⚛️  QUANTUM GRPC SERVICE v2.0  ⚛️                      ║
║                                                           ║
║   🔮 Python quantum core + gRPC interface                ║
║   💜 Serving quantum randomness to Go API                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    port = os.getenv('GRPC_PORT', '50051')
    print(f"🚀 gRPC server starting on port {port}...")
    print("⚠️  Note: Run 'python -m grpc_tools.protoc' to generate stubs first!")
    
    # server.add_insecure_port(f'[::]:{port}')
    # server.start()
    # print(f"✅ Server listening on 0.0.0.0:{port}")
    # server.wait_for_termination()
    
    # Placeholder until protobuf generated
    print("💡 This is a skeleton! Generate protobuf stubs to run:")
    print("   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pkg/grpc/quantum.proto")


if __name__ == '__main__':
    serve()
