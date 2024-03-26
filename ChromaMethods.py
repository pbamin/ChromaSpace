import openai
import streamlit as st
import json

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

        return colors,description
    
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
