import streamlit as st
from PIL import Image
import numpy as np
import cv2
import easyocr

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

# Title and file uploader
st.title('Image Resizing with OpenCV and OCR')
img_file_buffer = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# If an image is uploaded
if img_file_buffer is not None:
    image = np.array(Image.open(img_file_buffer))
    st.image(image, caption="Original Image", use_column_width=True)

    # Image Resizing Options
    useWH = st.checkbox('Resize using a Custom Height and Width')
    useScaling = st.checkbox('Resize using a Scaling Factor')

    if useWH:
        st.subheader('Input a new Width and Height')
        width = int(st.number_input('Input a new Width', value=720))
        height = int(st.number_input('Input a new Height', value=720))
        points = (width, height)
        
        resized_image = process_image(image, points)
        st.image(resized_image, caption="Resized Image", use_column_width=False)
    elif useScaling:
        st.subheader('Drag the Slider to change the Image Size')
        scaling_factor = st.slider('Resize the image using scaling factor', min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        
        resized_image = process_scaled_image(image, scaling_factor)
        st.image(resized_image, caption="Resized Image Using Scaling Factor", use_column_width=False)

    # OCR Feature
    st.subheader("OCR - Extract Text")
    if st.button("Run OCR"):
        ocr_reader = initialize_ocr()
        ocr_result = ocr_reader.readtext(image)

        extracted_text = "\n".join([text[1] for text in ocr_result])
        st.text_area("Extracted Text", extracted_text, height=200)
else:
    st.write("Please upload an image to continue.")
