from .client import client

def generate_image(story_text, name):
    image_prompt = (
        f"A doodle-style illustration based on this story: '{story_text}' "
        f"with the character's name as '{name}'. "
        "Use thick black outlines, flat pastel colors, and a playful Korean hand-drawn style."
    )
    response = client.images.generate(
        prompt=image_prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url if response.data else None
    return {"raw_image_response": response, "image_url": image_url}