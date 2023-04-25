#IMPORTS
import openai
import json
import os
from PIL import Image 
import IPython.display as display
from io import BytesIO
import requests
from requests.structures import CaseInsensitiveDict
import streamlit as st

#API KEY
openai.api_key = "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"
openai.__version__ = "0.10.2"

#HEADER
st.title('Image Generation Through Text Description Using OpenAI')
st.sidebar.header("Description")
st.sidebar.info("This WebApp uses OpenAI to generate images through texts.") 

#MAIN FUNCTION
def generate_image(prompt):
  model = "image-alpha-001"
  data = {
      "model": model,
      "prompt": prompt,
      "num_images": 1,
      "size": "512x512",
  }
  headers = CaseInsensitiveDict()
  headers["Content-Type"] = "application/json"
  headers["Authorization"] = f"Bearer {openai.api_key}"
  
  resp = requests.post("https://api.openai.com/v1/images/generations", headers=headers, data=json.dumps(data))

  if resp.status_code != 200:
    raise ValueError("Failed to generate image")

  response_text = json.loads(resp.text)
  image_url = response_text['data'][0]['url']
  image_data = requests.get(image_url).content
  image = Image.open(BytesIO(image_data))
  return image

# Title of the app
st.title("OpenAI Image Generator")

# Get user input
prompt = st.text_input("Enter a prompt to generate an image")

if prompt:
  # Generate the image
  generated_image = generate_image(prompt)

  # Display the image
  st.image(generated_image, caption="Generated Image")
