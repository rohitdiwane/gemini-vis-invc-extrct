from dotenv import load_dotenv 
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai

load_dotenv() 

os.getenv("genai_api_key")
genai.configure(api_key=os.getenv("genai_api_key"))

## Function to load OpenAI model and get respones

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



##initialize our streamlit app

st.set_page_config(page_title="Gemini-Vision-Demo")

st.header("Invoice Extracted Application")
input=st.text_input("Input-Prompt: ",key="input")
uploaded_file = st.file_uploader("Please choose an image file ...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the image")

input_prompt = """
               You are an expert in interpreting invoices. you will receive a invoice images as input and 
               can provide detailed answers to questions based on the information within those images.
               """

## If ask button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)