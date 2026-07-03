from dotenv import load_dotenv
import streamlit as st
import time
import os

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# -------------------- ENV --------------------
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    st.error("Missing GROQ_API_KEY in .env file")
    st.stop()

# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")
st.title("🚀 AI  Assistant")
st.caption("How can I help you today?")

# -------------------- SESSION STATE --------------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}
    st.session_state.active_chat = "Chat 1"

# -------------------- LLM (cached) --------------------
@st.cache_resource
def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.0,
    )

llm = get_llm()

# -------------------- SIDEBAR --------------------
st.sidebar.title("💬 Chats")

# New Chat
if st.sidebar.button("➕ New Chat"):
    new_chat = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat] = []
    st.session_state.active_chat = new_chat
    st.rerun()

# Delete Chat
if st.sidebar.button("🗑️ Delete Chat"):
    current = st.session_state.active_chat
    if current in st.session_state.chats:
        del st.session_state.chats[current]

    if st.session_state.chats:
        st.session_state.active_chat = list(st.session_state.chats.keys())[0]
    else:
        st.session_state.chats = {"Chat 1": []}
        st.session_state.active_chat = "Chat 1"

    st.rerun()

# Delete All Chats
if st.sidebar.button("️ 🗑️ Delete All Chats"):
    st.session_state.chats = {"Chat 1": []}
    st.session_state.active_chat = "Chat 1"
    st.rerun()

# Select chat
chat_list = list(st.session_state.chats.keys())
selected_chat = st.sidebar.radio("Select Chat", chat_list)
st.session_state.active_chat = selected_chat

# -------------------- CHAT DISPLAY --------------------
chat_history = st.session_state.chats[st.session_state.active_chat]

for msg in chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------- INPUT --------------------
user_prompt = st.chat_input("Ask something...")

if user_prompt:
    # show user
    with st.chat_message("user"):
        st.markdown(user_prompt)

    chat_history.append({"role": "user", "content": user_prompt})

    # convert to LangChain format
    messages = [SystemMessage(content="You are a helpful assistant.")]

    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    # -------------------- TIMER + SPINNER --------------------
    import time

    with st.spinner("🤖 Thinking..."):
        time.sleep(5)
        response = llm.invoke(messages)

    assistant_response = response.content

    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )
