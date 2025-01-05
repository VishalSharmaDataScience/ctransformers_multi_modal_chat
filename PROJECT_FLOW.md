# Project Flows

## Overview
This document provides an in-depth explanation of the various workflows and interconnections in the multimodal AI chatbot project. The chatbot integrates multiple features such as audio transcription, PDF analysis, and image processing into a unified interface, offering an engaging and efficient user experience.

---

## Flow 1: User Interaction and Chat Handling

### Key Components:
1. **`app.py`**: Acts as the main entry point for the Streamlit application, orchestrating the UI and backend logic.
2. **`llm_chains.py`**: Contains the logic to initialize and manage chat chains, which handle both normal and document-specific interactions.
3. **`html_templates.py`**: Responsible for generating the HTML templates used to render user and bot messages.
4. **`utils.py`**: Manages session histories by saving and loading chat data.

### Process:
1. **User Input**:
   - Users can interact with the chatbot by typing messages in the chatbox or uploading files (audio, images, PDFs).
   - Input is captured via Streamlit's widgets and stored in session state variables.
2. **Session State Management**:
   - The application keeps track of user inputs, chat history, and operational modes (e.g., normal chat or PDF-specific chat) using session state.
3. **Chat Chain Handling**:
   - If the user toggles PDF chat mode, the `load_pdf_chat_chain` function is called to handle PDF-related queries.
   - For all other inputs, the `load_normal_chain` function initializes a standard conversational chain.
4. **Rendering Responses**:
   - User and bot messages are formatted using templates from `html_templates.py` for consistent styling.
   - The chat history is saved periodically using `save_chat_history_json` to ensure continuity.

---

## Flow 2: Audio Processing

### Key Components:
1. **`audio_handler.py`**: Handles audio file uploads and transcribes them into text using Whisper AI.
2. **`llm_chains.py`**: Processes the transcribed text through a standard chat chain.

### Process:
1. **Audio File Upload**:
   - Users upload audio files (e.g., `.wav`, `.mp3`) via the Streamlit interface.
   - Uploaded files are passed to `convert_bytes_to_array`, which converts the raw audio bytes into an array for processing.
2. **Transcription**:
   - The `transcribe_audio` function utilizes Whisper AI to convert audio data into a textual format.
   - Whisper’s transcription is chunked into manageable segments for better accuracy.
3. **Chat Interaction**:
   - The transcribed text is fed into the chat chain via `load_chain`.
   - The chatbot generates responses contextualized by the transcribed content.
4. **Error Handling**:
   - Exception handling ensures that corrupted or unsupported audio files do not disrupt the workflow.

---

## Flow 3: PDF Analysis

### Key Components:
1. **`pdf_handler.py`**: Extracts text from PDF files and organizes it into chunks for analysis.
2. **`llm_chains.py`**: Integrates vector databases to enable retrieval-based querying.

### Process:
1. **PDF Upload**:
   - Users upload one or more PDF files through the Streamlit sidebar.
   - The `extract_text_from_pdf` function extracts raw text from the PDF pages.
2. **Text Chunking**:
   - Extracted text is split into smaller, manageable chunks using `get_text_chunks`.
   - These chunks are converted into document objects for structured storage.
3. **Database Storage**:
   - Documents are added to a vector database using `add_documents_to_db`.
   - The database enables quick retrieval of relevant sections during queries.
4. **Query Execution**:
   - The chatbot leverages `load_pdf_chat_chain` to match user queries with relevant text from the database.
   - It formulates responses by combining retrieved text with conversational context.

---

## Flow 4: Image Processing

### Key Components:
1. **`image_handler.py`**: Manages image data processing and generates detailed descriptions of uploaded images.
2. **`app.py`**: Interfaces with the Streamlit frontend to facilitate image uploads.

### Process:
1. **Image Upload**:
   - Users upload images via the Streamlit sidebar.
   - The image data is converted into a base64 format using `convert_bytes_to_base64` for compatibility with downstream processing.
2. **Image Analysis**:
   - The `handle_image` function processes the base64-encoded image using the Llava model.
   - The chatbot generates detailed descriptions, such as object detection, scene understanding, or visual summaries.
3. **Response Presentation**:
   - Image descriptions are displayed in the chat interface as part of the bot’s response to user input.
4. **Error Handling**:
   - Ensures unsupported or corrupted image formats are gracefully handled with user-friendly error messages.

---

## Flow 5: Chat History Management

### Key Components:
1. **`utils.py`**: Handles JSON-based saving and retrieval of chat histories.

### Process:
1. **Saving Chat History**:
   - Chat history is saved periodically to JSON files using `save_chat_history_json`.
   - Each session is uniquely identified by a timestamp generated via `get_timestamp`.
2. **Restoring Chat History**:
   - When a session is reopened, `load_chat_history_json` restores the previous conversation state.
   - This ensures seamless continuity for returning users.
3. **Data Integrity**:
   - Validates the existence of chat history files and prevents overwriting existing sessions.

---

## Flow 6: Model Initialization and Configuration

### Key Components:
1. **`config.yaml`**: Centralizes model paths, embedding configurations, and other settings.
2. **`llm_chains.py`**: Initializes language models and embeddings.

### Process:
1. **Configuration Loading**:
   - Model paths, embedding parameters, and runtime configurations are loaded from `config.yaml`.
   - Exception handling ensures that missing or malformed configuration files are flagged.
2. **Model Creation**:
   - The `create_llm` function initializes the primary language model using the loaded settings.
   - Similarly, `create_embeddings` sets up embedding models for vector-based retrieval tasks.
3. **Chain Assembly**:
   - Standard conversational chains and retrieval-based chains are assembled using initialized models, memory modules, and prompts.
   - This modular approach ensures flexibility for handling diverse user inputs.

---

## Summary
This project orchestrates multiple workflows into a unified, interactive chatbot application. Each flow operates independently yet integrates seamlessly with others to deliver a robust multimodal experience. Detailed error handling, modular architecture, and session management ensure a user-friendly and reliable system. Future expansions can focus on integrating additional modalities and enhancing the performance of the underlying AI models.

