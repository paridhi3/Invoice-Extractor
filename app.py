from dotenv import load_dotenv
load_dotenv()      # loading all environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load Gemini Pro Model and get responses
model = genai.GenerativeModel('gemini-pro-vision')
def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Multi-language Invoice Extractor")
st.header("Multi-language Invoice Extractor")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Initialize session state for chat history visibility if it doesn't exist
if 'show_chat_history' not in st.session_state:
    st.session_state['show_chat_history'] = False

input = st.text_input("Input: ", key="input")
uploaded_file = st.file_uploader("Upload invoice image: ", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

input_prompt = """
You are an expert in understanding invoices. An invoice image will be uploaded and 
you will answer every question related to the invoice.
"""

submit = st.button("Submit")
# When submit is clicked
if submit and uploaded_file:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)  
    
    # Append user input and response to chat history
    st.session_state['chat_history'].append(("You", input))
    st.session_state['chat_history'].append(("BOT", response))
    
    st.subheader("Answer")
    st.write(response)

# Button to toggle chat history visibility
if st.button("Show Chat History"):
    if not st.session_state['chat_history']:
        st.write("No chat history yet.")
    else:
        st.session_state['show_chat_history'] = not st.session_state['show_chat_history']

# Only display chat history if the button has been toggled to show
if st.session_state['show_chat_history'] and st.session_state['chat_history']:
    st.subheader("Chat History:")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
