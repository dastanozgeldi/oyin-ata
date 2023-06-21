import os
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


def init():
    load_dotenv()

    # Load the OpenAI API key from the .env file
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title="Your own ChatGPT",
        page_icon="🤖",
    )


def main():
    init()

    chat = ChatOpenAI(temperature=0)

    messages = [
        SystemMessage(content="You are a helpful assistant."),
    ]

    st.header("Your own ChatGPT 🤖")

    with st.sidebar:
        user_input = st.text_input("Your message", key="user_input")

    if user_input:
        message(user_input, is_user=True)
        messages.append(HumanMessage(content=user_input))
        response = chat(messages)
        message(response.content, is_user=False)


if __name__ == "__main__":
    main()
