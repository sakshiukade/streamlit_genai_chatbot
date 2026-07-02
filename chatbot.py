import time
from dotenv import load_dotenv
import streamlit as st
from pypdf import PdfReader
from langchain_groq import ChatGroq

# Load API Key
load_dotenv()

st.set_page_config(
    page_title="AI Assistant",
    page_icon="👩🏻‍💻",
    layout="wide"
)
if st.button("➕ New Chat"):
    st.session_state.chat_history = []
    st.rerun()
st.title("👩🏻‍💻 AI Assistant")
st.caption("Powered by Groq + LangChain")

with st.sidebar:
    st.header("About")
    st.write("💬 Ask any question")
    st.write("⚡ Powered by Llama 3.3")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
        with st.spinner("🤖 Thinking..."):
            response = llm.invoke(st.session_state.chat_history)
with st.sidebar:

                uploaded_files = st.file_uploader(
                    "Upload Images, PDFs, CSVs, or Text Files",
                    type=["png", "jpg", "jpeg", "pdf", "csv", "txt", "docx"],
                    accept_multiple_files=True
                )
pdf_text = ""

if uploaded_files is not None:
    for uploaded_file in uploaded_files:

        if uploaded_file.name.endswith(".pdf"):

            reader = PdfReader(uploaded_file)

            for page in reader.pages:
                if page.extract_text():
                    pdf_text += page.extract_text() + "\n"

    if pdf_text:
        st.sidebar.success("✅ PDF uploaded successfully!")
    else:
        st.sidebar.warning("⚠️ No text found in the PDF.")
with st.sidebar:
    if st.button("Recent"):

        st.title("Recent Chats")

        if "chat_history" in st.session_state:

            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        else:
            st.write("No recent chats.")
        #with st.sidebar:
    #st.button("Recent")

# Create LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
chat = ""

for message in st.session_state.chat_history:
    chat += f"{message['role']} : {message['content']}\n\n"

st.sidebar.download_button(
    "📥 Download Chat",
    chat,
    file_name="chat_history.txt"
)
# Show Old Messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
prompt = st.chat_input("Ask me anything...")

# When User Sends Message
if prompt:

    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save User Message
    st.session_state.chat_history.append(
        {"role": "user", "content": prompt}
    )

    # AI Response
    with st.chat_message("assistant"):

        # Thinking...
        with st.spinner("🤖 Thinking..."):
            time.sleep(2)

            response = llm.invoke(st.session_state.chat_history)
            st.code(response.content)


        # Show Answer
        st.markdown(response.content)

    # Save AI Message
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response.content}
    )