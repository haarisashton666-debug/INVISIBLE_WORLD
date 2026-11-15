import streamlit as st
import numpy as np
from PIL import Image, ImageFilter

st.title("Invisible Cloak")
st.write("Step 1: Photo of the background WITHOUT you.")
st.write("Step 2: Photo of you holding a RED cloth.")

bg_file = st.camera_input("Step 1: Background only")
fg_file = st.camera_input("Step 2: You with red cloth")

if bg_file and fg_file:
    img = Image.open(fg_file).convert("RGB")
    bg = Image.open(bg_file).convert("RGB").resize(img.size)

    hsv = np.array(img.convert("HSV")).astype(int)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    # red hue sits at both ends of the hue range
    mask = ((h <= 14) | (h >= 241)) & (s > 120) & (v > 70)

    mask_img = Image.fromarray((mask * 255).astype("uint8"))
    mask_img = mask_img.filter(ImageFilter.MinFilter(3))   # remove noise
    mask_img = mask_img.filter(ImageFilter.MaxFilter(7))   # fill gaps

    result = Image.composite(bg, img, mask_img)
    st.image(result, caption="Invisible cloak result")
