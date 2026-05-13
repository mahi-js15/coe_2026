# app.py

import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO

st.set_page_config(page_title="AI Image Enhancer", page_icon="✨")

st.title("✨ AI Image Enhancer")
st.write("Upload an image and enhance brightness, sharpness, and quality.")

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------------
# IMAGE ENHANCEMENT FUNCTION
# -----------------------------------
def enhance_image(image):

    # Increase sharpness
    sharp_enhancer = ImageEnhance.Sharpness(image)
    image = sharp_enhancer.enhance(2.0)

    # Increase contrast
    contrast_enhancer = ImageEnhance.Contrast(image)
    image = contrast_enhancer.enhance(1.5)

    # Increase brightness
    brightness_enhancer = ImageEnhance.Brightness(image)
    image = brightness_enhancer.enhance(1.2)

    # Smooth image slightly
    image = image.filter(ImageFilter.SMOOTH)

    return image

# -----------------------------------
# DOWNLOAD FUNCTION
# -----------------------------------
def convert_image(image):

    buffer = BytesIO()

    image.save(buffer, format="PNG")

    byte_data = buffer.getvalue()

    return byte_data

# -----------------------------------
# MAIN APP
# -----------------------------------
if uploaded_file is not None:

    original_image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(original_image, use_container_width=True)

    if st.button("✨ Enhance Image"):

        enhanced_image = enhance_image(original_image)

        st.subheader("Enhanced Image")
        st.image(enhanced_image, use_container_width=True)

        image_download = convert_image(enhanced_image)

        st.download_button(
            label="⬇ Download Enhanced Image",
            data=image_download,
            file_name="enhanced_image.png",
            mime="image/png"
        )
