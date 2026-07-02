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

st.title("AI Assistant")
st.caption("Powered by Groq + LangChain")
with st.sidebar:
    st.title("🤖 Chatbot")  # Sidebar title
    st.write("Welcome!")  # Welcome message
    st.info("Ask me anything about Python, SQL, Power BI, AI, etc.")  # User guidance

    # Sidebar
    with st.sidebar:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                }
            ]
            st.rerun()
st.subheader("💡 Try asking")  # Suggestion section
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=120)
    st.title("AI Chatbot")
    st.write("Powered by Groq")
    st.write("Model: Llama 3.3")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):  # with : context manger everything belong to that chat bubble
        st.markdown(message["content"])
        import time
        with st.spinner("💭 Thinking..."):
            time.sleep(6)  # Wait for 15 seconds
            response = "This is a demo chatbot response."
# Create LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile", #3 we can use different model from groq
    temperature=0.0,## controls randomness
)

# User input
user_prompt = st.chat_input("PROMPT...")

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

