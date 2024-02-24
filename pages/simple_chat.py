import streamlit as st
import openai

st.title('Simple Chat')

user_message = st.text_input(label='どうしましたか?')

if user_message:
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]
    )

    st.write(completion)