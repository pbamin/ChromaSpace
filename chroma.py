import os
import openai
import json
from IPython.display import Markdown
import cv2
from PIL import Image
import numpy as np
import streamlit as st
from ChromaMethods import ChromaMethods as cm

openai.api_key = st.secrets["OPEN_API_KEY"]

def main():
    # Custom title "ChromaSpace" with interesting font and color
    st.markdown("<h1 style='text-align: center; color: #FF5733; font-family: cursive;'>ChromaSpace</h1>", unsafe_allow_html=True)

    # Slogan below the title
    st.markdown("<h3 style='text-align: center; color: #3366FF;'>Unleash Your Design with ChromaSpace: Where Ideas Bloom into Beautiful Spaces</h3>", 
                unsafe_allow_html=True)

    # Rest of the Streamlit app code remains the same

     # Input for user message
    user_message = st.text_input("Enter your theme/description:")

    # Button to trigger the AI color palette suggestion
    if st.button("Get Color Palette"):
        color_block, colors, description = cm.palette_ai(user_message)
        
        # Display the color block and description
        st.subheader("Generated Color Palette:")
        cm.color_block(colors, description)

        # Display the color palette as color swatches
        st.subheader("Color Swatches:")
        for color in colors:
            st.markdown(f'<span style="color:{color}">{chr(9608)*4}</span>', unsafe_allow_html=True)
    
    # Input for uploading the room image
    room_image = st.file_uploader("Upload an image of your room", type=["jpg", "jpeg", "png"])

    # Input for room dimensions
    room_dimensions_provided = st.radio("Do you have the room's height, width, and length?", ('Yes', 'No')) == 'Yes'
    if room_dimensions_provided:
        height = st.number_input("Enter room height (meters)", value=0.0, step=0.1)
        width = st.number_input("Enter room width (meters)", value=0.0, step=0.1)
        length = st.number_input("Enter room length (meters)", value=0.0, step=0.1)
    else:
        height, width, length = None, None, None

    # Generate the text prompt
    text_prompt = cm.generate_text_prompt(room_image, height, width, length)

    # Display the generated text prompt
    st.subheader("Generated Text Prompt:")
    st.write(text_prompt)
    
if __name__=="__main__":
    main()
