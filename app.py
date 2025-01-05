import streamlit as st
from llm_chains import load_normal_chain, load_pdf_chat_chain
from langchain.memory import StreamlitChatMessageHistory
from streamlit_mic_recorder import mic_recorder
from utils import save_chat_history_json, get_timestamp, load_chat_history_json
from image_handler import handle_image
from audio_handler import transcribe_audio
from pdf_handler import add_documents_to_db
import yaml
import os

from html_templates import get_bot_template, get_user_template, css

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def load_chain(chat_history):
    """
    Load a chat chain based on the current state of the pdf_chat checkbox.

    If the pdf_chat checkbox is checked, load a pdf chat chain, otherwise load
    a normal chat chain.

    Args:
        chat_history (list[ChatMessage]): The chat history.

    Returns:
        ChatChain: The loaded chat chain.
    """
    if st.session_state.pdf_chat:
        print("loading pdf chat chain")
        return load_pdf_chat_chain(chat_history)
    return load_normal_chain(chat_history)

def clear_input_field():
    """
    Clear the user input field.

    If the user has typed something in the input field, save it in the
    user_question session state variable and clear the user_input session
    state variable.
    """
    if st.session_state.user_question == "":
        # Save the user's input in case they want to reuse it later
        st.session_state.user_question = st.session_state.user_input
        # Clear the input field
        st.session_state.user_input = ""

def set_send_input() -> None:
    """
    Set the send_input session state variable to True and clear the user input
    field.

    This function is called when the user clicks the send button. It sets the
    send_input session state variable to True and clears the user input field
    by calling the clear_input_field function.
    """
    st.session_state.send_input = True
    clear_input_field()

def toggle_pdf_chat():
    """
    Toggle the pdf_chat checkbox to True.

    This function is used in the Streamlit interface to toggle the PDF Chat
    checkbox. It is called when the user selects the PDF Chat option from the
    dropdown menu.
    """
    st.session_state.pdf_chat = True

def save_chat_history():
    """
    Save the current chat history to a JSON file.

    This function is called when the user wants to save the current chat
    history to a JSON file. It checks if the chat history is not empty and
    if the session key is "new_session". If so, it generates a new filename
    by concatenating the current timestamp with ".json" and saves the chat
    history to the file. If the session key is not "new_session", it simply
    saves the chat history to the file with the same name as the session key.
    """
    # Check if the chat history is not empty
    if st.session_state.history != []:
        # Check if the session key is "new_session"
        if st.session_state.session_key == "new_session":
            # Generate a new filename by concatenating the current timestamp with ".json"
            st.session_state.new_session_key = get_timestamp() + ".json"
            # Save the chat history to the new file
            save_chat_history_json(st.session_state.history, config["chat_history_path"] + st.session_state.new_session_key)
        else:
            # Save the chat history to the file with the same name as the session key
            save_chat_history_json(st.session_state.history, config["chat_history_path"] + st.session_state.session_key)

            
def main():
    """
    Main function to run the Streamlit app for the Multimodal Local Chat App.
    
    This function sets up the Streamlit interface, manages session states,
    handles user inputs, and processes uploaded files.
    """
    st.title("Multimodal AI Chat")
    st.write(css, unsafe_allow_html=True)
    
    # Set up sidebar for chat sessions
    st.sidebar.title("Chat Sessions")
    chat_sessions = ["new_session"] + os.listdir(config["chat_history_path"])

    # Initialize session state variables
    if "send_input" not in st.session_state:
        st.session_state.session_key = "new_session"
        st.session_state.send_input = False
        st.session_state.user_question = ""
        st.session_state.new_session_key = None
        st.session_state.session_index_tracker = "new_session"
    
    # Track session key updates
    if st.session_state.session_key == "new_session" and st.session_state.new_session_key is not None:
        st.session_state.session_index_tracker = st.session_state.new_session_key
        st.session_state.new_session_key = None

    # Set up session selection in sidebar
    index = chat_sessions.index(st.session_state.session_index_tracker)
    st.sidebar.selectbox("Select a chat session", chat_sessions, key="session_key", index=index)
    st.sidebar.toggle("PDF Chat", key="pdf_chat", value=False)

    # Load chat history based on session key
    if st.session_state.session_key != "new_session":
        st.session_state.history = load_chat_history_json(config["chat_history_path"] + st.session_state.session_key)
    else:
        st.session_state.history = []

    # Initialize chat history
    chat_history = StreamlitChatMessageHistory(key="history")
    
    # User input field
    user_input = st.text_input("Type your message here", key="user_input", on_change=set_send_input)

    # Layout for voice recording and send button
    voice_recording_column, send_button_column = st.columns(2)
    chat_container = st.container()
    with voice_recording_column:
        voice_recording = mic_recorder(start_prompt="Start recording", stop_prompt="Stop recording", just_once=True)
    with send_button_column:
        send_button = st.button("Send", key="send_button", on_click=clear_input_field)

    # File uploaders for audio, image, and PDF files
    uploaded_audio = st.sidebar.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"])
    uploaded_image = st.sidebar.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
    uploaded_pdf = st.sidebar.file_uploader("Upload a pdf file", accept_multiple_files=True, key="pdf_upload", type=["pdf"], on_change=toggle_pdf_chat)

    # Process uploaded PDF files
    if uploaded_pdf:
        with st.spinner("Processing pdf..."):
            add_documents_to_db(uploaded_pdf)

    # Process uploaded audio files
    if uploaded_audio:
        transcribed_audio = transcribe_audio(uploaded_audio.getvalue())
        print(transcribed_audio)
        llm_chain = load_chain(chat_history)
        llm_chain.run("Summarize this text: " + transcribed_audio)

    # Process voice recordings
    if voice_recording:
        transcribed_audio = transcribe_audio(voice_recording["bytes"])
        print(transcribed_audio)
        llm_chain = load_chain(chat_history)
        llm_chain.run(transcribed_audio)

    # Handle send button click and user input
    if send_button or st.session_state.send_input:
        if uploaded_image:
            with st.spinner("Processing image..."):
                user_message = "Describe this image in detail please."
                if st.session_state.user_question != "":
                    user_message = st.session_state.user_question
                    st.session_state.user_question = ""
                llm_answer = handle_image(uploaded_image.getvalue(), user_message)
                chat_history.add_user_message(user_message)
                chat_history.add_ai_message(llm_answer)

        if st.session_state.user_question != "":
            llm_chain = load_chain(chat_history)
            llm_response = llm_chain.run(st.session_state.user_question)
            st.session_state.user_question = ""

        st.session_state.send_input = False

    # Display chat history
    if chat_history.messages:
        with chat_container:
            st.write("Chat History:")
            for message in reversed(chat_history.messages):
                if message.type == "human":
                    st.write(get_user_template(message.content), unsafe_allow_html=True)
                else:
                    st.write(get_bot_template(message.content), unsafe_allow_html=True)

    # Save chat history
    save_chat_history()

if __name__ == "__main__":
    main()