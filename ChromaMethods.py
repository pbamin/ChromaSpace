import openai
import streamlit as st
import json
from PIL import Image, ImageDraw

openai.api_key = st.secrets["OPEN_API_KEY"]

class ChromaMethods:

    def palette_ai(user_message):
        
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
                "content": f'{user_message}'
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

        return colors,description
    
    def arrange_ai(user_message, client, room_image, room_width, room_length, room_height):
        prompt = f"{user_message} Photorealistic image of a well-furnished room that resembles the uploaded image (if provided)."
        if room_width:
            prompt += f" The room width is approximately {room_width:.2f} meters."
        if room_length:
            prompt += f" The room length is approximately {room_length:.2f} meters."
        if room_height:
            prompt += f" The room height is approximately {room_height:.2f} meters."

        arrange_response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        image_url = arrange_response.data[0].url
        return image_url
