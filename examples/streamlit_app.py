"""
Quantum-Seed ImageShield - Streamlit Demo Interface

A user-friendly interface for quantum-enhanced image encryption.
Upload images, apply quantum encryption, and visualize results with statistical metrics.
"""

import streamlit as st
import numpy as np
from PIL import Image
import io
import sys
import os

# Add parent directory to path to import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from the unified package
from quantum_image_shield import QuantumKeyGenerator, ImageEncryptor, ImageDecryptor
from quantum_image_shield.analysis import (
    analyze_image,
    calculate_psnr,
    generate_histogram_plot,
    generate_correlation_plot
)


# Helper functions for the Streamlit app
def load_image_as_grayscale(image_path_or_bytes):
    """Load an image and convert to grayscale numpy array."""
    if isinstance(image_path_or_bytes, bytes):
        image = Image.open(io.BytesIO(image_path_or_bytes))
    else:
        image = Image.open(image_path_or_bytes)
    grayscale = image.convert('L')
    return np.array(grayscale, dtype=np.uint8)


def array_to_image_bytes(image_array):
    """Convert numpy array to image bytes (for Streamlit display)."""
    image = Image.fromarray(image_array.astype(np.uint8), mode='L')
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    return buf.getvalue()


def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="Quantum-Seed ImageShield",
        page_icon="🔐",
        layout="wide"
    )
    
    # Title and description
    st.title("🔐 Quantum-Seed ImageShield")
    st.markdown("""
    ### Hybrid Quantum-Classical Image Encryption System
    
    This system leverages **quantum-generated randomness** to enhance security in digital image encryption.
    Using IBM's Qiskit platform, we generate truly random keys through quantum circuits,
    then apply classical encryption techniques (XOR operations and pixel permutations).
    """)
    
    # Sidebar for options
    st.sidebar.header("Settings")
    use_seed = st.sidebar.checkbox("Use seed for reproducibility", value=False)
    seed_value = None
    if use_seed:
        seed_value = st.sidebar.number_input("Seed value", value=42, min_value=0)
    
    show_advanced = st.sidebar.checkbox("Show advanced metrics", value=True)
    
    # File uploader
    st.header("1. Upload Image")
    uploaded_file = st.file_uploader(
        "Choose a grayscale image (or any image - will be converted to grayscale)",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff']
    )
    
    if uploaded_file is not None:
        # Load and display original image
        image_bytes = uploaded_file.read()
        original_array = load_image_as_grayscale(image_bytes)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Original Image")
            st.image(original_array, caption="Original Image", use_container_width=True)
            st.write(f"Size: {original_array.shape[1]} × {original_array.shape[0]} pixels")
        
        # Generate quantum keys and encrypt
        st.header("2. Quantum Key Generation & Encryption")
        
        if st.button("🔑 Generate Quantum Keys & Encrypt", type="primary"):
            with st.spinner("Generating quantum keys using Qiskit..."):
                # Use the unified package's array-based API
                encryptor = ImageEncryptor(quantum_seed=seed_value if use_seed else None)
                encrypted_array = encryptor.encrypt_array(original_array)
                
                # Get the keys that were generated
                xor_key, permutation_key = encryptor.get_last_keys()
                
                # Store in session state
                st.session_state.xor_key = xor_key
                st.session_state.permutation_key = permutation_key
                st.session_state.encrypted_array = encrypted_array
                st.session_state.original_array = original_array
                
                st.success("✅ Quantum keys generated and image encrypted!")
                st.write(f"XOR key length: {len(xor_key)} bytes")
                st.write(f"Permutation key size: {len(permutation_key)} elements")
        
        # Display encrypted image if available
        if 'encrypted_array' in st.session_state:
            with col2:
                st.subheader("Encrypted Image")
                st.image(
                    st.session_state.encrypted_array,
                    caption="Encrypted Image",
                    use_container_width=True
                )
            
            # Decrypt button
            st.header("3. Decryption")
            if st.button("🔓 Decrypt Image"):
                with st.spinner("Decrypting image..."):
                    # Use the unified package's array-based decryption
                    decryptor = ImageDecryptor()
                    decrypted_array = decryptor.decrypt_array(
                        st.session_state.encrypted_array,
                        st.session_state.xor_key,
                        st.session_state.permutation_key
                    )
                    
                    st.session_state.decrypted_array = decrypted_array
                    st.success("✅ Image decrypted successfully!")
            
            # Display decrypted image if available
            if 'decrypted_array' in st.session_state:
                with col3:
                    st.subheader("Decrypted Image")
                    st.image(
                        st.session_state.decrypted_array,
                        caption="Decrypted Image",
                        use_container_width=True
                    )
                
                # Calculate PSNR
                psnr = calculate_psnr(
                    st.session_state.original_array,
                    st.session_state.decrypted_array
                )
                if np.isinf(psnr):
                    st.success("🎉 Perfect reconstruction! PSNR = ∞ (identical to original)")
                else:
                    st.info(f"PSNR: {psnr:.2f} dB")
            
            # Analysis section
            st.header("4. Statistical Analysis")
            
            # Analyze original image
            st.subheader("Original Image Analysis")
            original_metrics = analyze_image(st.session_state.original_array)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Entropy", f"{original_metrics['entropy']:.4f} bits")
            with col2:
                st.metric("Uniformity", f"{original_metrics['uniformity']:.4f}")
            with col3:
                st.metric(
                    "Avg Correlation",
                    f"{np.mean([original_metrics['correlation_horizontal'], original_metrics['correlation_vertical'], original_metrics['correlation_diagonal']]):.4f}"
                )
            
            # Analyze encrypted image
            st.subheader("Encrypted Image Analysis")
            encrypted_metrics = analyze_image(st.session_state.encrypted_array)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Entropy",
                    f"{encrypted_metrics['entropy']:.4f} bits",
                    delta=f"{encrypted_metrics['entropy'] - original_metrics['entropy']:.4f}"
                )
            with col2:
                st.metric(
                    "Uniformity",
                    f"{encrypted_metrics['uniformity']:.4f}",
                    delta=f"{encrypted_metrics['uniformity'] - original_metrics['uniformity']:.4f}"
                )
            with col3:
                st.metric(
                    "Avg Correlation",
                    f"{np.mean([encrypted_metrics['correlation_horizontal'], encrypted_metrics['correlation_vertical'], encrypted_metrics['correlation_diagonal']]):.4f}",
                    delta=f"{np.mean([encrypted_metrics['correlation_horizontal'], encrypted_metrics['correlation_vertical'], encrypted_metrics['correlation_diagonal']]) - np.mean([original_metrics['correlation_horizontal'], original_metrics['correlation_vertical'], original_metrics['correlation_diagonal']]):.4f}",
                    delta_color="inverse"
                )
            
            # Histogram comparison
            st.subheader("Histogram Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Original Image Histogram**")
                hist_original = generate_histogram_plot(
                    st.session_state.original_array,
                    "Original Image Histogram"
                )
                st.image(hist_original)
            
            with col2:
                st.write("**Encrypted Image Histogram**")
                hist_encrypted = generate_histogram_plot(
                    st.session_state.encrypted_array,
                    "Encrypted Image Histogram"
                )
                st.image(hist_encrypted)
            
            # Advanced metrics
            if show_advanced:
                st.subheader("Advanced Correlation Analysis")
                
                st.write("**Correlation between adjacent pixels**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("*Original Image - Horizontal Correlation*")
                    corr_plot_orig = generate_correlation_plot(
                        st.session_state.original_array,
                        'horizontal',
                        f"Original (r={original_metrics['correlation_horizontal']:.4f})"
                    )
                    st.image(corr_plot_orig)
                
                with col2:
                    st.write("*Encrypted Image - Horizontal Correlation*")
                    corr_plot_enc = generate_correlation_plot(
                        st.session_state.encrypted_array,
                        'horizontal',
                        f"Encrypted (r={encrypted_metrics['correlation_horizontal']:.4f})"
                    )
                    st.image(corr_plot_enc)
                
                # Detailed metrics table
                st.write("**Detailed Metrics Comparison**")
                metrics_data = {
                    "Metric": [
                        "Entropy (bits)",
                        "Uniformity",
                        "Horizontal Correlation",
                        "Vertical Correlation",
                        "Diagonal Correlation"
                    ],
                    "Original": [
                        f"{original_metrics['entropy']:.4f}",
                        f"{original_metrics['uniformity']:.4f}",
                        f"{original_metrics['correlation_horizontal']:.4f}",
                        f"{original_metrics['correlation_vertical']:.4f}",
                        f"{original_metrics['correlation_diagonal']:.4f}"
                    ],
                    "Encrypted": [
                        f"{encrypted_metrics['entropy']:.4f}",
                        f"{encrypted_metrics['uniformity']:.4f}",
                        f"{encrypted_metrics['correlation_horizontal']:.4f}",
                        f"{encrypted_metrics['correlation_vertical']:.4f}",
                        f"{encrypted_metrics['correlation_diagonal']:.4f}"
                    ]
                }
                st.table(metrics_data)
    
    else:
        st.info("👆 Please upload an image to begin")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### About This System
    
    **Quantum-Seed ImageShield** demonstrates the practical application of quantum computing in cryptography:
    
    - 🔬 **Quantum Key Generation**: Uses Hadamard gates and measurements to generate truly random keys
    - 🔐 **XOR Encryption**: Applies quantum keystream to pixel values
    - 🔄 **Pixel Permutation**: Shuffles pixel positions for additional security
    - 📊 **Statistical Analysis**: Evaluates encryption quality through multiple metrics
    
    **Key Indicators of Strong Encryption:**
    - ✅ Higher entropy (closer to 8 bits for 8-bit images)
    - ✅ More uniform histogram
    - ✅ Lower correlation between adjacent pixels
    - ✅ Perfect PSNR after decryption (∞ dB)
    """)


if __name__ == "__main__":
    main()
