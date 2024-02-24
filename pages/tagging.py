import streamlit as st
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain_pydantic

class Attribute(BaseModel):
    language: str = Field(enum=["ja","en"])
    tags: list[str] = Field(examples=[["Python", "Streamlit"]])

st.title("タグ付け")

text = st.text_area(label="タグ付けするテキスト")

if text:
    with st.spinner("タグ付け中..."):
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        chain = create_tagging_chain_pydantic(Attribute, llm)
        attr = chain.run(text)
        st.write(attr)