"""
Quantum-Seed ImageShield - Streamlit Demo Interface

A user-friendly interface for quantum-enhanced image encryption.
Upload images, apply quantum encryption, and visualize results with statistical metrics.
"""

import streamlit as st
import numpy as np
from PIL import Image
import io

# Import our modules
from quantum_key_generator import generate_quantum_key
from image_encryptor import (
    ImageEncryptor, 
    load_image_as_grayscale, 
    array_to_image_bytes
)
from image_analysis import (
    analyze_image,
    calculate_psnr,
    generate_histogram_plot,
    generate_correlation_plot
)


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
    
    # Tabs for Encrypt/Decrypt
    tab_encrypt, tab_decrypt = st.tabs(["Encrypt Image", "Decrypt Image"])

    # ENCRYPT TAB
    with tab_encrypt:
        st.header("1. Upload Image to Encrypt")
        uploaded_file = st.file_uploader(
            "Choose a grayscale image (or any image - will be converted to grayscale)",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            key="encrypt_uploader"
        )

        st.sidebar.header("Encryption Settings")
        use_seed = st.sidebar.checkbox("Use seed for reproducibility", value=False)
        seed_value = st.sidebar.number_input("Seed value", value=42, min_value=0) if use_seed else None
        show_advanced = st.sidebar.checkbox("Show advanced metrics", value=True)

        if uploaded_file is not None:
            image_bytes = uploaded_file.read()
            original_array = load_image_as_grayscale(image_bytes)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Original Image")
                st.image(original_array, caption="Original Image", use_container_width=True)
                st.write(f"Size: {original_array.shape[1]} × {original_array.shape[0]} pixels")

            st.header("2. Quantum Key Generation & Encryption")
            if st.button("🔑 Generate Quantum Keys & Encrypt", type="primary", key="encrypt_btn"):
                with st.spinner("Generating quantum keys using Qiskit..."):
                    image_size = original_array.size
                    keystream, permutation_seed = generate_quantum_key(
                        image_size,
                        seed=seed_value if use_seed and seed_value is not None else None
                    )
                    st.session_state.keystream = keystream
                    st.session_state.permutation_seed = permutation_seed
                    st.success("✅ Quantum keys generated successfully!")
                    st.write(f"Keystream length: {len(keystream)} bytes")
                    st.write(f"Permutation seed: {permutation_seed}")

                with st.spinner("Encrypting image..."):
                    encryptor = ImageEncryptor(keystream, permutation_seed)
                    encrypted_array = encryptor.encrypt_image(original_array)
                    st.session_state.encrypted_array = encrypted_array
                    st.session_state.original_array = original_array
                    st.success("✅ Image encrypted successfully!")

            if 'encrypted_array' in st.session_state:
                import tempfile
                import base64
                # Download encrypted image
                with col2:
                    st.subheader("Encrypted Image")
                    st.image(
                        st.session_state.encrypted_array,
                        caption="Encrypted Image",
                        use_container_width=True
                    )
                    # Prepare encrypted image bytes
                    encrypted_img_bytes = array_to_image_bytes(st.session_state.encrypted_array)
                    st.download_button(
                        label="Download Encrypted Image (PNG)",
                        data=encrypted_img_bytes,
                        file_name="encrypted_image.png",
                        mime="image/png"
                    )
                    # Prepare .npz key file
                    with tempfile.NamedTemporaryFile(suffix=".npz", delete=False) as tmpkey:
                        np.savez_compressed(
                            tmpkey,
                            xor_key=st.session_state.keystream,
                            permutation_key=st.session_state.permutation_seed,
                            shape=np.array(st.session_state.encrypted_array.shape)
                        )
                        tmpkey.flush()
                        tmpkey.seek(0)
                        key_bytes = tmpkey.read()
                    st.download_button(
                        label="Download Key File (.npz)",
                        data=key_bytes,
                        file_name="encryption_keys.npz",
                        mime="application/octet-stream"
                    )

                st.header("3. Decryption (Session)")
                if st.button("🔓 Decrypt Image", key="decrypt_btn_session"):
                    with st.spinner("Decrypting image..."):
                        encryptor = ImageEncryptor(
                            st.session_state.keystream,
                            st.session_state.permutation_seed
                        )
                        decrypted_array = encryptor.decrypt_image(
                            st.session_state.encrypted_array
                        )
                        st.session_state.decrypted_array = decrypted_array
                        st.success("✅ Image decrypted successfully!")

                if 'decrypted_array' in st.session_state:
                    with col3:
                        st.subheader("Decrypted Image")
                        st.image(
                            st.session_state.decrypted_array,
                            caption="Decrypted Image",
                            use_container_width=True
                        )
                    psnr = calculate_psnr(
                        st.session_state.original_array,
                        st.session_state.decrypted_array
                    )
                    if np.isinf(psnr):
                        st.success("🎉 Perfect reconstruction! PSNR = ∞ (identical to original)")
                    else:
                        st.info(f"PSNR: {psnr:.2f} dB")

                # Analysis section (same as before)
                st.header("4. Statistical Analysis")
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

    # DECRYPT TAB
    with tab_decrypt:
        st.header("1. Upload Encrypted Image & Key File")
        encrypted_file = st.file_uploader(
            "Upload encrypted image",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            key="decrypt_img_uploader"
        )
        key_file = st.file_uploader(
            "Upload key file (.npz)",
            type=['npz'],
            key="decrypt_key_uploader"
        )

        if encrypted_file is not None and key_file is not None:
            encrypted_bytes = encrypted_file.read()
            encrypted_array = load_image_as_grayscale(encrypted_bytes)
            key_data = np.load(key_file)
            keystream = key_data['xor_key']
            permutation_key = key_data['permutation_key']
            shape = tuple(key_data['shape'])
            # Reshape encrypted array if needed
            if encrypted_array.shape != shape:
                encrypted_array = encrypted_array.reshape(shape)

            st.subheader("Encrypted Image Preview")
            st.image(encrypted_array, caption="Encrypted Image", use_container_width=True)

            if st.button("� Decrypt Uploaded Image", key="decrypt_btn_uploaded"):
                with st.spinner("Decrypting uploaded image..."):
                    encryptor = ImageEncryptor(keystream, permutation_key)
                    decrypted_array = encryptor.decrypt_image(encrypted_array)
                    st.session_state.decrypted_uploaded_array = decrypted_array
                    st.success("✅ Uploaded image decrypted!")

            if 'decrypted_uploaded_array' in st.session_state:
                st.subheader("Decrypted Image Preview")
                st.image(st.session_state.decrypted_uploaded_array, caption="Decrypted Image", use_container_width=True)
        else:
            st.info("👆 Please upload both encrypted image and key file to decrypt.")
    
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
