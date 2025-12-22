import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# App title
st.set_page_config(page_title="AI Career Guidance Chatbot", page_icon="🎓")
st.title("🎓 AI Career Guidance Chatbot")
st.write("Ask me anything about careers, internships, or skills in computer science.")

# System prompt
SYSTEM_PROMPT = """
You are a helpful and professional career guidance assistant for computer science students.
You provide advice on internships, entry-level roles, skills to learn, learning resources, and career paths in technology.
Your responses should be clear, concise, supportive, and practical.
If you do not know an answer, say so honestly.
"""

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )

            assistant_reply = response.choices[0].message.content
            response_placeholder.markdown(assistant_reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_reply}
            )

        except Exception as e:
            response_placeholder.error("Error generating response. Please check your API key.")
