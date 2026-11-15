import streamlit as st
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from io import BytesIO

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="INVISIBLE WORLD",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# FUTURISTIC DESIGN
# -----------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071426, #101e35);
    color: white;
}

section[data-testid="stSidebar"] {
    background: #0b1930;
}

h1, h2, h3 {
    color: #45d9ff !important;
}

p, label {
    color: #e0eaf5;
}

div[data-testid="stMetric"] {
    background: #142b46;
    border: 1px solid #237ca5;
    padding: 16px;
    border-radius: 12px;
}

.stButton button {
    background: #087da8;
    color: white;
    border-radius: 10px;
    border: none;
}

hr {
    border-color: #237ca5;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------
# HEADER
# -----------------------------------

st.markdown(
    "<h1 style='text-align:center;'>🌌 INVISIBLE WORLD</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>"
    "AI VISION SCANNER | SCIENTIFIC IMAGE ANALYSIS"
    "</p>",
    unsafe_allow_html=True
)

st.divider()


# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🌌 NAVIGATION")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Photo Scanner",
        "About Project"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Explore image properties using "
    "computer vision technology."
)


# -----------------------------------
# HOME PAGE
# -----------------------------------

if page == "Home":

    st.subheader("Welcome to Invisible World")

    st.write(
        "Explore the hidden details of ordinary "
        "photographs through scientific image processing."
    )

    st.markdown("### Available Technologies")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📷 CAMERA SCANNER\n\nCapture photographs.")

    with col2:
        st.info("🔬 IMAGE PROCESSING\n\nAnalyse image structures.")

    with col3:
        st.info("📊 DATA ANALYTICS\n\nGenerate scientific measurements.")

    st.divider()

    st.subheader("How it works")

    st.write("""
    1. Open the Photo Scanner.
    2. Capture a photograph or upload an image.
    3. The system processes the image.
    4. View grayscale and edge detection results.
    5. Explore analytical measurements.
    6. Download your analysis report.
    """)

    if st.button("OPEN PHOTO SCANNER"):
        st.session_state["open_scanner"] = True
        st.rerun()


# -----------------------------------
# PHOTO SCANNER
# -----------------------------------

elif page == "Photo Scanner" or (
    page == "Home" and st.session_state.get("open_scanner", False)
):

    st.subheader("📷 Advanced Photo Scanner")

    st.write(
        "Capture an image using your camera "
        "or upload an existing photograph."
    )

    input_method = st.radio(
        "Choose image source",
        ["Camera", "Upload Image"],
        horizontal=True
    )

    uploaded_image = None

    if input_method == "Camera":

        uploaded_image = st.camera_input(
            "Take a photograph"
        )

    else:

        uploaded_image = st.file_uploader(
            "Upload a photograph",
            type=["jpg", "jpeg", "png", "webp"]
        )

    if uploaded_image is not None:

        try:
            image = Image.open(uploaded_image)
            image = ImageOps.exif_transpose(image).convert("RGB")
            image_array = np.array(image)

            # Image processing
            gray = cv2.cvtColor(
                image_array,
                cv2.COLOR_RGB2GRAY
            )

            edges = cv2.Canny(
                gray,
                100,
                200
            )

            height, width, channels = image_array.shape

            brightness = float(np.mean(gray))

            contrast = float(np.std(gray))

            edge_percentage = float(
                np.count_nonzero(edges) / edges.size * 100
            )

            average_red = float(np.mean(image_array[:, :, 0]))
            average_green = float(np.mean(image_array[:, :, 1]))
            average_blue = float(np.mean(image_array[:, :, 2]))

            # IMAGE DISPLAY
            st.divider()

            st.subheader("Captured Photograph")

            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    image_array,
                    caption="Original Photograph",
                    use_container_width=True
                )

            with col2:
                st.image(
                    edges,
                    caption="Edge Detection Result",
                    use_container_width=True,
                    clamp=True
                )

            # ANALYTICAL DATA
            st.divider()

            st.subheader("📊 Scientific Analysis")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Width", f"{width} px")
            c2.metric("Height", f"{height} px")
            c3.metric("Brightness", f"{brightness:.2f}/255")
            c4.metric("Contrast", f"{contrast:.2f}")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Edge Percentage",
                f"{edge_percentage:.2f}%"
            )

            c2.metric(
                "Total Pixels",
                f"{width * height:,}"
            )

            c3.metric(
                "Image Channels",
                str(channels)
            )

            # GRAYSCALE
            st.divider()

            st.subheader("🔬 Grayscale Analysis")

            st.image(
                gray,
                caption="Grayscale Processed Image",
                use_container_width=True,
                clamp=True
            )

            # COLOUR ANALYSIS
            st.divider()

            st.subheader("🎨 RGB Colour Analysis")

            color_data = pd.DataFrame({
                "Colour": ["Red", "Green", "Blue"],
                "Average Intensity": [
                    average_red,
                    average_green,
                    average_blue
                ]
            })

            st.bar_chart(
                color_data.set_index("Colour")
            )

            # HISTOGRAM
            st.divider()

            st.subheader("📈 Image Intensity Histogram")

            fig, ax = plt.subplots(figsize=(10, 4))

            ax.hist(
                gray.ravel(),
                bins=256,
                range=(0, 256)
            )

            ax.set_xlabel("Pixel Intensity")
            ax.set_ylabel("Number of Pixels")
            ax.set_title("Grayscale Intensity Distribution")
            ax.set_xlim(0, 255)

            fig.patch.set_alpha(0)
            ax.set_facecolor("#142b46")
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")

            st.pyplot(fig)
            plt.close(fig)

            # AUTOMATIC OBSERVATIONS
            st.divider()

            st.subheader("🧠 Analytical Observations")

            if brightness < 85:
                st.warning("The image has relatively low brightness.")

            elif brightness > 180:
                st.info("The image has relatively high brightness.")

            else:
                st.success("The image has moderate brightness.")

            if contrast < 35:
                st.info("The image has relatively low contrast.")

            else:
                st.success("The image has noticeable contrast.")

            st.write(
                f"Approximately {edge_percentage:.2f}% "
                "of pixels were identified as edges "
                "by the selected edge detector."
            )

            # REPORT DOWNLOAD
            st.divider()

            st.subheader("📥 Download Analysis Report")

            report = pd.DataFrame({
                "Parameter": [
                    "Image Width",
                    "Image Height",
                    "Total Pixels",
                    "Brightness",
                    "Contrast",
                    "Edge Percentage",
                    "Average Red",
                    "Average Green",
                    "Average Blue"
                ],
                "Value": [
                    width,
                    height,
                    width * height,
                    brightness,
                    contrast,
                    edge_percentage,
                    average_red,
                    average_green,
                    average_blue
                ]
            })

            csv_data = report.to_csv(index=False)

            st.download_button(
                "DOWNLOAD CSV REPORT",
                data=csv_data,
                file_name="invisible_world_report.csv",
                mime="text/csv"
            )

            # Download processed image
            edge_image = Image.fromarray(edges)

            image_buffer = BytesIO()
            edge_image.save(image_buffer, format="PNG")

            st.download_button(
                "DOWNLOAD EDGE IMAGE",
                data=image_buffer.getvalue(),
                file_name="edge_analysis.png",
                mime="image/png"
            )

            st.success("Image analysis completed successfully!")

        except Exception as error:
            st.error(f"Image processing error: {error}")


# -----------------------------------
# ABOUT PAGE
# -----------------------------------

elif page == "About Project":

    st.subheader("About Invisible World")

    st.write("""
    INVISIBLE WORLD is a scientific exploration
    platform designed to analyse photographs
    through digital image processing.

    The current version uses:

    - Python
    - Streamlit
    - OpenCV
    - NumPy
    - Pandas
    - Matplotlib
    - Pillow

    Future development can include:

    - AI object recognition
    - Thermal sensor integration
    - Magnetic sensor integration
    - Light intensity measurement
    - 3D scientific visualisation
    - Scan history and reports
    """)

    st.info(
        "Version 1.0 | Invisible World Scientific Project"
    )
