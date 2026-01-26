import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


GROQ_API_KEY = "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"  
client = Groq(api_key=GROQ_API_KEY)

# Page Config
st.set_page_config(
    page_title="NexChat AI", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

#  CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f8fafc;
    }
    
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* Message Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        transition: transform 0.2s ease;
    }
    .stChatMessage:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.08);
    }

    /* Buttons Styling */
    .stButton > button {
        border-radius: 12px;
        border: none;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }

    /* Header Text */
    h1 {
        background: linear-gradient(to right, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Header
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("🤖NexChat")
    st.caption("High-Performance AI")
    
    st.markdown("### 🛠️ Workspace")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ New Chat"):
            st.session_state.messages = [{"role": "system", "content": "You are NexChat AI, a brilliant and helpful assistant."}]
            st.rerun()
    with col2:
        if st.button("🧹 Clear"):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    if "messages" in st.session_state:
        st.write(f"Messages: {len(st.session_state.messages) - 1}")
    
    # Export Option
    if st.button("📥 Export Conversation"):
        chat_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        st.download_button("Confirm Download", chat_history, file_name="nexchat_log.txt")

    st.markdown("---")
    st.info("Developed by Shibin Oommen")

# Main Interface
st.title("🤖 NexChat")
st.markdown("##### *Elevate your workflow with intelligent conversation.*")

# Initialize Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are NexChat AI, the ultimate conversation partner. Be brilliant, helpful, and engaging."}]

# Display Chat
for msg in st.session_state.messages[1:]:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Chat Input & Logic
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages,
                stream=True,
                temperature=0.7,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {e}")
            full_response = "I encountered an error connecting to the engine."

    st.session_state.messages.append({"role": "assistant", "content": full_response})
