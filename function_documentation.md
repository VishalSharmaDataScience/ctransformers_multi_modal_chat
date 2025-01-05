# Function Documentation

## Overview
This document provides an enhanced overview of the functions implemented in the project files, their purposes, their arguments, and how they are interconnected. Each function plays a specific role in creating a seamless multimodal AI chat application that supports audio transcription, image analysis, and PDF interaction.

---

## File: `prompt_templates.py`

### Functions:
1. **`memory_prompt_template`**
   - **Purpose**: Provides a template for the chatbot to recall previous conversations and generate context-aware responses.
   - **Arguments**:
     - None (defined as a static template).
   - **Connections**: Used by `llm_chains.py` to create prompts for chat interactions.

---

## File: `llm_chains.py`

### Functions:
1. **`create_llm`**
   - **Purpose**: Initializes the language model (LLM) using configurations provided in `config.yaml`.
   - **Arguments**:
     - `model_path` (str): Path to the LLM model.
     - `model_type` (str): Type of the LLM.
     - `model_config` (dict): Configuration dictionary for the LLM.
   - **Connections**: Used by both `chatChain` and `pdfChatChain` classes to initialize the language model.

2. **`create_embeddings`**
   - **Purpose**: Generates embeddings using a HuggingFace model.
   - **Arguments**:
     - `embeddings_path` (str): Path to the embeddings model.
   - **Connections**: Essential for `load_vectordb` and `pdfChatChain` to create vector databases for document retrieval.

3. **`create_chat_memory`**
   - **Purpose**: Creates a memory object to track chat history.
   - **Arguments**:
     - `chat_history` (list): List of previous chat messages.
   - **Connections**: Utilized by both `chatChain` and `pdfChatChain` to maintain session context.

4. **`create_prompt_from_template`**
   - **Purpose**: Constructs a prompt using a provided template.
   - **Arguments**:
     - `template` (str): Template string for constructing the prompt.
   - **Connections**: Integrates with `memory_prompt_template` to structure LLM interactions.

5. **`create_llm_chain`**
   - **Purpose**: Combines LLM, prompt, and memory into a functional chain.
   - **Arguments**:
     - `llm` (object): The language model instance.
     - `chat_prompt` (PromptTemplate): Prompt for the chain.
     - `memory` (object): Memory object for storing context.
   - **Connections**: Used by `chatChain` for generating responses.

6. **`load_normal_chain`**
   - **Purpose**: Loads a basic chat chain without document retrieval capabilities.
   - **Arguments**:
     - `chat_history` (list): Chat history for the chain.
   - **Connections**: Called in `app.py` for general chat interactions.

7. **`load_vectordb`**
   - **Purpose**: Loads a vector database for embeddings storage and retrieval.
   - **Arguments**:
     - `embeddings` (object): Embedding function for the vector database.
   - **Connections**: Supports `pdfChatChain` for document-based interactions.

8. **`load_pdf_chat_chain`**
   - **Purpose**: Creates a specialized chain for PDF interactions.
   - **Arguments**:
     - `chat_history` (list): Chat history for the chain.
   - **Connections**: Invoked in `app.py` when PDF chat mode is toggled.

9. **`load_retrieval_chain`**
   - **Purpose**: Loads a chain for retrieval-based QA tasks.
   - **Arguments**:
     - `llm` (object): Language model.
     - `memory` (object): Memory object.
     - `vector_db` (object): Vector database instance.
   - **Connections**: Combines LLM, memory, and vector database for document querying.

10. **`pdfChatChain` (Class)**
    - **Purpose**: Handles chat interactions based on PDF content.
    - **Key Methods**: `__init__`, `run`.
    - **Connections**: Depends on `load_vectordb`, `create_embeddings`, and `create_llm` for its operation.

11. **`chatChain` (Class)**
    - **Purpose**: Handles general chat interactions.
    - **Key Methods**: `__init__`, `run`.
    - **Connections**: Integrates with `create_llm`, `create_prompt_from_template`, and `create_llm_chain` for generating responses.

---

## File: `config.yaml`

### Purpose:
- Configuration file specifying model paths, types, and parameters.
- **Connections**: Referenced throughout the project to configure models and chat history paths.

---

## File: `audio_handler.py`

### Functions:
1. **`convert_bytes_to_array`**
   - **Purpose**: Converts audio file bytes to an array for processing.
   - **Arguments**:
     - `audio_bytes` (bytes): Raw audio bytes.
   - **Connections**: Prepares audio data for `transcribe_audio`.

2. **`transcribe_audio`**
   - **Purpose**: Transcribes audio to text using Whisper AI.
   - **Arguments**:
     - `audio_bytes` (bytes): Raw audio bytes.
   - **Connections**: Provides transcribed text to `load_chain` in `app.py` for response generation.

---

## File: `pdf_handler.py`

### Functions:
1. **`get_pdf_texts`**
   - **Purpose**: Extracts text from multiple PDF files.
   - **Arguments**:
     - `pdfs_bytes_list` (list): List of PDF files in byte format.
   - **Connections**: Initial step for `add_documents_to_db` to prepare text for vectorization.

2. **`extract_text_from_pdf`**
   - **Purpose**: Extracts text from a single PDF file.
   - **Arguments**:
     - `pdf_bytes` (bytes): Single PDF file in byte format.
   - **Connections**: Supports `get_pdf_texts` for text extraction.

3. **`get_text_chunks`**
   - **Purpose**: Splits text into manageable chunks.
   - **Arguments**:
     - `text` (str): Raw text to be chunked.
   - **Connections**: Prepares text for `get_document_chunks`.

4. **`get_document_chunks`**
   - **Purpose**: Converts text chunks into document objects.
   - **Arguments**:
     - `text_list` (list): List of text chunks.
   - **Connections**: Provides input for `add_documents_to_db`.

5. **`add_documents_to_db`**
   - **Purpose**: Adds document chunks to the vector database.
   - **Arguments**:
     - `pdfs_bytes` (list): List of PDFs in byte format.
   - **Connections**: Enables `pdfChatChain` to perform document-based queries.

---

## File: `app.py`

### Functions:
1. **`load_chain`**
   - **Purpose**: Loads either a normal or PDF-based chat chain depending on the session state.
   - **Arguments**:
     - `chat_history` (list): Chat history for the chain.
   - **Connections**: Calls `load_normal_chain` or `load_pdf_chat_chain` based on user interaction.

2. **`clear_input_field`**
   - **Purpose**: Clears the user input field in the UI.
   - **Arguments**:
     - None.

3. **`set_send_input`**
   - **Purpose**: Prepares user input for submission.
   - **Arguments**:
     - None.

4. **`toggle_pdf_chat`**
   - **Purpose**: Activates PDF-based chat mode.
   - **Arguments**:
     - None.
   - **Connections**: Sets the session state to use `pdfChatChain`.

5. **`save_chat_history`**
   - **Purpose**: Saves the chat history to a file.
   - **Arguments**:
     - None.
   - **Connections**: Relies on `utils.py` functions for JSON handling.

6. **`main`**
   - **Purpose**: Entry point for the Streamlit app.
   - **Arguments**:
     - None.
   - **Connections**: Coordinates UI components and backend logic, linking all major functions.

---

## File: `html_templates.py`

### Functions:
1. **`get_bot_template`**
   - **Purpose**: Generates HTML for bot messages.
   - **Arguments**:
     - `MSG` (str): Message text to display.
   - **Connections**: Used in `app.py` for rendering bot responses.

2. **`get_user_template`**
   - **Purpose**: Generates HTML for user messages.
   - **Arguments**:
     - `MSG` (str): Message text to display.
   - **Connections**: Used in `app.py` for rendering user inputs.

---

## File: `image_handler.py`

### Functions:
1. **`convert_bytes_to_base64`**
   - **Purpose**: Converts image bytes to a base64 string.
   - **Arguments**:
     - `image_bytes` (bytes): Raw image bytes.
   - **Connections**: Prepares image data for `handle_image`.

2. **`handle_image`**
   - **Purpose**: Processes an image and generates a detailed description.
   - **Arguments**:
     - `image_bytes` (bytes): Raw image bytes.
     - `user_message` (str): User's message to guide image analysis.
   - **Connections**: Supplies image descriptions to `app.py` for chat responses.

3. **`convert_image_to_base64`**
   - **Purpose**: Converts an image file to a base64 string.
   - **Arguments**:
     - `image_path` (str): Path to the image file.

---

## File: `utils.py`

### Functions:
1. **`save_chat_history_json`**
   - **Purpose**: Saves chat history as a JSON file.
   - **Arguments**:
     - `chat_history` (list): Chat history to save.
     - `file_path` (str): Path to the output JSON file.
   - **Connections**: Called by `save_chat_history` in `app.py`.

2. **`load_chat_history_json`**
   - **Purpose**: Loads chat history from a JSON file.
   - **Arguments**:
     - `file_path` (str): Path to the input JSON file.
   - **Connections**: Used in `app.py` to restore previous sessions.

3. **`get_timestamp`**
   - **Purpose**: Generates a timestamp for session tracking.
   - **Arguments**:
     - None.
   - **Connections**: Utilized in `app.py` for naming chat history files.

---

## File: `requirements.txt`

### Purpose:
- Lists the dependencies required to run the project.
- **Connections**: Ensures all necessary libraries are installed for the application to function.

---

This document is intended to serve as a comprehensive guide for developers and collaborators to understand the project’s structure, how the functions interact, their arguments, and their interdependencies.

