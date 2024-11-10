import streamlit as st
from PIL import Image
import numpy as np
import cv2
import easyocr

# Set background image using custom CSS
bg_image_url = "https://raw.githubusercontent.com/ansabb420/CV_lab/main/BG.jpg"  # Updated URL
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{bg_image_url}');
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize OCR reader
@st.cache_resource
def initialize_ocr():
    return easyocr.Reader(['en'])

# Image resizing functions
@st.cache
def process_image(image, points):
    resized_img = cv2.resize(image, points, interpolation=cv2.INTER_LINEAR)
    return resized_img

@st.cache
def process_scaled_image(image, scaling_factor):
    resized_img = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_LINEAR)
    return resized_img

# Title for the App
st.title('CV_Lab')

# Section 1: Image Resizing
st.header("Image Resizing with OpenCV")

# File uploader for resizing
img_file_buffer_resizing = st.file_uploader("Upload an image for resizing", type=["jpg", "jpeg", "png"], key="resizing")

# If an image is uploaded for resizing
if img_file_buffer_resizing is not None:
    image_resizing = np.array(Image.open(img_file_buffer_resizing))
    st.image(image_resizing, caption="Original Image for Resizing", use_column_width=True)

    # Image Resizing Options
    useWH = st.checkbox('Resize using a Custom Width and Height')
    useScaling = st.checkbox('Resize using a Scaling Factor')

    if useWH:
        st.subheader('Input a new Width and Height')
        width = int(st.number_input('Input a new Width', value=720, key="width"))
        height = int(st.number_input('Input a new Height', value=720, key="height"))
        points = (width, height)
        
        resized_image = process_image(image_resizing, points)
        st.image(resized_image, caption="Resized Image", use_column_width=False)

    elif useScaling:
        st.subheader('Drag the Slider to change the Image Size')
        scaling_factor = st.slider('Resize the image using scaling factor', min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        
        resized_image = process_scaled_image(image_resizing, scaling_factor)
        st.image(resized_image, caption="Resized Image Using Scaling Factor", use_column_width=False)

# Section 2: OCR
st.header("OCR - Text Extraction from Images")

# File uploader for OCR
img_file_buffer_ocr = st.file_uploader("Upload an image for OCR", type=["jpg", "jpeg", "png"], key="ocr")

# OCR button and functionality
if img_file_buffer_ocr is not None:
    image_ocr = Image.open(img_file_buffer_ocr)
    st.image(image_ocr, caption="Image for OCR", use_column_width=True)

    if st.button("Run OCR"):
        ocr_reader = initialize_ocr()
        ocr_result = ocr_reader.readtext(np.array(image_ocr))

        # Extract and display text
        extracted_text = "\n".join([text[1] for text in ocr_result])
        st.text_area("Extracted Text", extracted_text, height=200)
else:
    st.write("Please upload an image to run OCR.")
