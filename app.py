import io
import numpy as np
import streamlit as st
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

st.set_page_config(page_title="Invisible World")
st.title("Invisible World")
st.write("Take or upload any photo and see the hidden layers inside it.")

source = st.radio("Photo source", ["Camera", "Upload"], horizontal=True)
if source == "Camera":
    f = st.camera_input("Take a photo of any object")
else:
    f = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])


def to_img(arr):
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))


def hidden_details(img):
    arr = np.array(img).astype(float) / 255
    lifted = to_img(np.power(arr, 0.5) * 255)      # brighten shadows
    lifted = ImageOps.equalize(lifted)             # pull out faint detail
    return lifted.filter(ImageFilter.UnsharpMask(radius=3, percent=200, threshold=2))


def edges(img):
    g = ImageOps.grayscale(img).filter(ImageFilter.GaussianBlur(1))
    return ImageOps.autocontrast(g.filter(ImageFilter.FIND_EDGES), cutoff=1)


def xray(img):
    g = ImageOps.invert(ImageOps.equalize(ImageOps.grayscale(img)))
    a = np.array(g).astype(float) / 255
    return to_img(np.stack([a * 0.55, a * 0.85, a], axis=2) * 255)


def heatmap(img):
    g = np.array(ImageOps.autocontrast(ImageOps.grayscale(img))).astype(float) / 255
    r = np.clip(1.5 - np.abs(4 * g - 3), 0, 1)
    gr = np.clip(1.5 - np.abs(4 * g - 2), 0, 1)
    b = np.clip(1.5 - np.abs(4 * g - 1), 0, 1)
    return to_img(np.stack([r, gr, b], axis=2) * 255)


def lsb(img):
    return to_img((np.array(img) & 1) * 255)


def ela(img):
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=90)
    buf.seek(0)
    re = Image.open(buf).convert("RGB")
    d = np.abs(np.array(img).astype(int) - np.array(re).astype(int))
    return to_img(d * (255.0 / max(d.max(), 1)))


def channel(img, i):
    return Image.fromarray(np.array(img)[..., i])


if f:
    img = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
    img.thumbnail((900, 900))

    tabs = st.tabs(["Original", "Hidden details", "Outlines", "X-ray",
                    "Heat map", "Hidden pixels", "Edited areas", "Colour layers"])

    with tabs[0]:
        st.image(img, caption="Original photo")
    with tabs[1]:
        st.image(hidden_details(img), caption="Shadows lifted, faint details pulled out")
    with tabs[2]:
        st.image(edges(img), caption="Every edge and outline in the photo")
    with tabs[3]:
        st.image(xray(img), caption="X-ray style view (inverted, contrast boosted)")
    with tabs[4]:
        st.image(heatmap(img), caption="Heat-map style view of brightness (not real temperature)")
    with tabs[5]:
        st.image(lsb(img), caption="Least significant bits. Patterns here can mean data hidden in the image")
    with tabs[6]:
        st.image(ela(img), caption="Error level analysis. Brighter patches may be edited or pasted areas")
    with tabs[7]:
        c1, c2, c3 = st.columns(3)
        c1.image(channel(img, 0), caption="Red layer")
        c2.image(channel(img, 1), caption="Green layer")
        c3.image(channel(img, 2), caption="Blue layer")
else:
    st.info("Take or upload a photo to begin.")
