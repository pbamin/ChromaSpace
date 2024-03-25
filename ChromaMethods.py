class ChromaMethods:

    system_prompt = f"""
    You are an ai color generator,
    based on the user's description,
    you will suggest a visually aesthetic color combination suitable for interior design
    in a json array of hexcodes.
    """

    def color_block(colors,description):
        color_block="".join(f'<span style="color:{color}">{chr(9608)*4}</span>'for color in colors)
        display(Markdown(f"**{description}**<br/>{color_block}"))

    def palette_ai(msg):
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
    
        color_block(colors,description)

        return color_block,colors,description
    
    def generate_text_prompt(self, room_image, height=None, width=None, length=None, desired_furniture=""):
        prompt = "Photorealistic image of a well-furnished room that resembles the one in the attached image. "
        if room_image is not None:
            prompt += f"The room dimensions are approximately {height:.2f} meters high, {width:.2f} meters wide, and {length:.2f} meters long (if provided). "
        prompt += f"The furniture arrangement is optimized for {desired_furniture} activities."
        return prompt
    
    text_prompt = generate_text_prompt(room_image, height, width, length)
    print(f"Generated text prompt:\n{text_prompt}")