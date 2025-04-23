import streamlit as st
from PIL import Image
import io

st.title("Image Cropper")

# Sidebar input for aspect ratio
st.sidebar.header("Crop Settings")

preset_options = {
    "16:9 (Widescreen)": (16, 9),
    "21:9 (Ultrawide or CinemaScope)": (21, 9),
    "4:3 (Standard or Fullscreen)": (4, 3),
    "3:2 (Classic or DSLR)": (3, 2),
    "5:4 (Large Format)": (5, 4),
    "2:1 (Univisium or Panoramic)": (2, 1),
    "1.85:1 (Academy Widescreen)": (1.85, 1),
    "2.39:1 (Anamorphic Widescreen)": (2.39, 1),
    "9:16 (Vertical Video)": (9, 16),
    "9:21 (Vertical Ultrawide)": (9, 21),
    "3:4 (Vertical Standard)": (3, 4),
    "2:3 (Vertical Classic)": (2, 3),
    "4:5 (Instagram Portrait)": (4, 5),
    "5:8 (Golden Ratio)": (5, 8),
    "3:5 (Film Portrait)": (3, 5)
}

preset_label = st.sidebar.selectbox("Choose a preset aspect ratio", list(preset_options.keys()))
width_ratio, height_ratio = preset_options[preset_label]

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    # Convert to custom aspect ratio by cropping
    width, height = image.size
    target_aspect_ratio = width_ratio / height_ratio
    current_aspect_ratio = width / height

    if current_aspect_ratio > target_aspect_ratio:
        # Image is too wide
        new_width = int(height * target_aspect_ratio)
        left = (width - new_width) // 2
        right = left + new_width
        top = 0
        bottom = height
    else:
        # Image is too tall
        new_height = int(width / target_aspect_ratio)
        top = (height - new_height) // 2
        bottom = top + new_height
        left = 0
        right = width

    cropped_image = image.crop((left, top, right, bottom))

    st.subheader(f"Cropped Image ({width_ratio}:{height_ratio})")
    st.image(cropped_image, use_container_width=True)

    # Save cropped image to in-memory file
    buf = io.BytesIO()
    cropped_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Cropped Image",
        data=byte_im,
        file_name="cropped_image.png",
        mime="image/png"
    )
