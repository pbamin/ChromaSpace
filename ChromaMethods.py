import openai
import streamlit as st
import json
from PIL import Image, ImageDraw

openai.api_key = st.secrets["OPEN_API_KEY"]

class ChromaMethods:

    def palette_ai(msg):
        
        system_prompt = f"""
        You are an ai color generator,
        based on the user's description,
        you will suggest a visually aesthetic color combination suitable for interior design
        in a json array of hexcodes.
        """
        chroma_response = openai.chat.completions.create(
            model ='gpt-3.5-turbo',
            messages=[{
                "role":"system",
                "content": system_prompt
            },
            {
                "role":"user",
                "content":"combination color for interior design"
            },
            {
                "role":"assistant",
                "content":'["#ECF8F8","#EEE4E1","#E7D8C9","#E6BEAE"]'
            },
            {
                "role":"user",
                "content": f'{msg}'
            }],
            max_tokens=150,
            temperature=0.9
        )

        print(chroma_response.choices[0].message.content)
        colors = json.loads(chroma_response.choices[0].message.content)
        description = openai.chat.completions.create(
            model='gpt-3.5-turbo', 
            messages=[{
                "role": "system",
                "content": "Please describe the following color palette relates to interior design in one sentence: {}".format(colors)
            }]
        ).choices[0].message.content

        return colors,description, ["#ECF8F8","#EEE4E1","#E7D8C9","#E6BEAE"]
    
    def generate_color_block_image(colors, output_path):
        # Define the size of the color block image
        block_size = 100
        image_width = block_size * len(colors)
        image_height = block_size

        # Create a new image with the specified size
        image = Image.new("RGB", (image_width, image_height), "white")
        draw = ImageDraw.Draw(image)

        # Draw rectangles for each color in the color block image
        for i, color in enumerate(colors):
            draw.rectangle([i * block_size, 0, (i + 1) * block_size, block_size], fill=color)

        # Save the image
        image.save(output_path)

        return output_path
    
    def arrange_ai(msg,client):
        arrange_response = client.images.generate(
            model="dall-e-2",
            prompt=f"{msg} Photorealistic image of a well-furnished room that based on user's descrition and the room's uploaded image, height, width and length",
            size="1024x1024",
            quality="standard",
            n=1,
            room_image=room_image,
            room_width=room_width,
            room_length=room_length,
            room_height=room_height
        )

        image_url = arrange_response.data[0].url
        return image_url
