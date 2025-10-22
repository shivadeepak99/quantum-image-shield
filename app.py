# app.py
import streamlit as st
import numpy as np
from utils import load_grayscale, save_grayscale, image_entropy, histogram_flatness, adjacent_pixel_correlation, psnr
from encryptor import QuantumSeedImageShield
from PIL import Image
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title='Quantum-Seed ImageShield', layout='wide')

st.title('Quantum-Seed ImageShield — Demo')
st.markdown('Hybrid quantum-classical image encryption with Qiskit randomness')

uploaded = st.file_uploader('Upload an image (PNG/JPG). For best results use a small grayscale image (e.g. 128x128).', type=['png', 'jpg', 'jpeg'])

if uploaded is not None:
    # read into PIL -> grayscale
    image = Image.open(uploaded).convert('L')
    arr = np.array(image)
    st.subheader('Original')
    st.image(arr, clamp=True, channels='L')

    if st.button('Encrypt with Quantum Seed'):
        shield = QuantumSeedImageShield(arr.shape)
        encrypted = shield.encrypt(arr)
        keys = shield.export_keys()

        st.subheader('Encrypted')
        st.image(encrypted, clamp=True, channels='L')

        st.markdown('**Metrics**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Entropy (original):', round(image_entropy(arr), 4))
            st.write('Entropy (encrypted):', round(image_entropy(encrypted), 4))
            st.write('PSNR (orig vs decrypted): computing after decryption')

            h = histogram_flatness(encrypted)
            fig, ax = plt.subplots()
            ax.plot(h)
            ax.set_title('Encrypted Image Histogram')
            st.pyplot(fig)

        with col2:
            corr_orig = adjacent_pixel_correlation(arr)
            corr_enc = adjacent_pixel_correlation(encrypted)
            st.write('Adjacent pixel correlation (original)', corr_orig)
            st.write('Adjacent pixel correlation (encrypted)', corr_enc)

        # allow user to decrypt
        if st.button('Decrypt using saved keys'):
            # Create a new shield and import keys
            shield2 = QuantumSeedImageShield(arr.shape)
            shield2.import_keys(keys)
            decrypted = shield2.decrypt(encrypted)
            st.subheader('Decrypted')
            st.image(decrypted, clamp=True, channels='L')
            st.write('PSNR:', psnr(arr, decrypted))
            st.write('Decryption identical to original?', bool(np.array_equal(arr, decrypted)))

        # option to download encrypted image
        buf = io.BytesIO()
        Image.fromarray(encrypted).save(buf, format='PNG')
        st.download_button('Download encrypted PNG', data=buf.getvalue(), file_name='encrypted.png', mime='image/png')
