from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Streamlit page
st.set_page_config(
    page_title="🗨 Chatbot",
    page_icon="💌",
    layout="centered"
)

st.title("🗨 Generative AI Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):  # with : context manger everything belong to that chat bubble
        st.markdown(message["content"])

# Create LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile", #3 we can use different model from groq
    temperature=0.0,## controls randomness
)

# User input
user_prompt = st.chat_input("Ask a question...")

if user_prompt:  ## runs only if user entered something

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save user message
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Get AI response
    response = llm.invoke(
        ## invoke : send request to model
        [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.content

    # Save assistant message
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(assistant_response)