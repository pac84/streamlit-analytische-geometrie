import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Analytische Geometrie",
    page_icon = "m"
)

st.write("# Berechnungen in der analytischen Geometrie")
st.markdown("""
Hier finden sich Berechnungen und Hilfen zur analytischen Geometrie. Auf der linken Seite findet sich ein Menü mit verschiedenen Anwendungen.
""")
image = Image.open('images/intro.png')
st.image(image)