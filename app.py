import streamlit as st
from PIL import Image
import cv2
import numpy as np
from io import BytesIO

st.set_page_config(page_title="AI Image Enhancer", page_icon="✨")

st.title("✨ AI Image Enhancer")
st.write("Upload a blurry or dark image and enhance it automatically.")

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------------
# IMAGE ENHANCEMENT FUNCTION
# -----------------------------------
def enhance_image(image):

    # Convert PIL to OpenCV
    img = np.array(image)

    # Convert RGB to BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Denoise image
    denoise = cv2.fastNlMeansDenoisingColored(
        img,
        None,
        10,
        10,
        7,
        21
    )

    # Sharpen image
    kernel = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ])

    sharpened = cv2.filter2D(denoise, -1, kernel)

    # Improve brightness and contrast
    enhanced = cv2.convertScaleAbs(
        sharpened,
        alpha=1.2,   # Contrast
        beta=20      # Brightness
    )

    # Convert back to RGB
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)

    return enhanced

# -----------------------------------
# DOWNLOAD FUNCTION
# -----------------------------------
def convert_image(img_array):

    image = Image.fromarray(img_array)

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
