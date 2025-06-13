'''import streamlit as st
st.title("Thummalkari Arlene")
user_input = st.text_input("what do you want")
if user_input:
    st.write(f"you said:{user_input}")
button = st.button("🎙️Listen")
if button:
    st.write("listening")
            '''
'''
import streamlit as st

# Set the app title
st.title("Chatbot Interface with Scrollable History")

# Initialize session state for mic status and user messages
if "mic_active" not in st.session_state:
    st.session_state.mic_active = False  # Default: Mic is OFF

if "messages" not in st.session_state:
    st.session_state.messages = []  # Store chat history

# Layout for input and mic button
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input("Type your message...", "")

with col2:
    if st.button("🎙️"):
        st.session_state.mic_active = not st.session_state.mic_active  # Toggle mic state

# Append user input to chat history
if user_input:
    st.session_state.messages.append(f"You said: {user_input}")

# Display scrollable chat history
st.text_area("Chat History:", "\n".join(st.session_state.messages), height=200)

# Show mic status within the text field dynamically
if st.session_state.mic_active:
    st.text_area("Chat History:", "\n".join(st.session_state.messages) + "\nListening...", height=200)
'''

import streamlit as st

# Set the app title
st.title("Chatbot Interface with Chat Above Input")

# Initialize session state for mic status and messages
if "mic_active" not in st.session_state:
    st.session_state.mic_active = False  # Default: Mic is OFF

if "messages" not in st.session_state:
    st.session_state.messages = []  # Store chat history

# Display chat history above the input field
st.text_area("Chat History:", "\n".join(st.session_state.messages), height=250, disabled=True)

# Layout for input and mic button
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input("Type your message...")

with col2:
    if st.button("🎙️"):
        st.session_state.mic_active = not st.session_state.mic_active  # Toggle mic state

# Append user input to chat history
if user_input:
    st.session_state.messages.append(f"You said: {user_input}")

# Update chat history dynamically when mic is active
if st.session_state.mic_active:
    st.session_state.messages.append("Listening...")

# Refresh chat history above the input field
st.text_area("Chat History:", "\n".join(st.session_state.messages), height=250, disabled=True)
