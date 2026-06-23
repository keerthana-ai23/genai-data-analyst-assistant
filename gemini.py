import streamlit as st
import google.generativeai as genai

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content(
    "Give me 3 insights about a sales dataset."
)

print(response.text)