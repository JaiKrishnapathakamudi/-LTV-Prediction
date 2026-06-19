from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)

print(response.choices[0].message.content)