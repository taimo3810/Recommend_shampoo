import streamlit as st
from image_generator import generate_image
# App title
st.title('Image Generator App')

# Text input for any required parameter (e.g., a prompt for the image generator)
user_input = st.text_input("Enter your prompt:", "A beautiful landscape")

# Button to generate image
if st.button('Generate Image'):
    # Here you would integrate your image generation model. For simplicity, we use a placeholder.
    # This is where you'd call your model, for example:
    st.write(f'Generating image for: {user_input}')
    # Display the image (using a placeholder here)
    image_url = generate_image(user_input)
    st.image(image_url, caption='Image from URL', width=20)
    # add image to library


