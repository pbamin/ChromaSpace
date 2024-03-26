import os
import openai
import json
from IPython.display import Markdown
from PIL import Image, ImageDraw
import streamlit as st
from ChromaMethods import ChromaMethods as cm

client = openai.OpenAI(api_key=st.secrets["OPEN_API_KEY"])

def main():
    # Custom title "ChromaSpace" with interesting font and color
    st.markdown("<h1 style='text-align: center; color: #FF5733; font-family: cursive;'>ChromaSpace</h1>", unsafe_allow_html=True)

    # Slogan below the title
    st.markdown("<h3 style='text-align: center; color: #3366FF;'>Unleash Your Design with ChromaSpace: Where Ideas Bloom into Beautiful Spaces</h3>", 
                unsafe_allow_html=True)

    # Input for user message
    user_message = st.text_input("Enter your theme/description:")

    if st.button("Generate Color Palette Hexcodes", key="generate_color_palette_button"):
        colors, description = cm.palette_ai(user_message)
        st.write("Generated Color Palette Hexcodes:")
        st.write(colors)
        st.write("Description:")
        st.write(description)
    
    # Input for uploading the room image
    room_image = st.file_uploader("Upload an image of your room", type=["jpg", "jpeg", "png"])

    # Input for room dimensions
    room_dimensions_provided = st.radio("Do you have the room's height, width, and length?", ('Yes', 'No')) == 'Yes'
    if room_dimensions_provided:
        room_height = st.slider("Room Height (meters)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        room_width = st.slider("Room Width (meters)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        room_length = st.slider("Room Length (meters)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
    else:
        room_length,room_width,room_height = None, None, None
    
    if st.button("Generate Arrangement"):
        if room_image is not None:
            # Assuming you have the 'client' object for image generation
            image_url = cm.arrange_ai(user_message, client, room_image, room_width, room_length, room_height)
            st.image(image_url, caption="Generated Image")
        else:
            st.write("Please upload an image of the room.")

if __name__=="__main__":
    main()
