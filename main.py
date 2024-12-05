import streamlit as st
import pyttsx3
import os
from gtts import gTTS
from datetime import datetime
from pathlib import Path

# Directory to store temporary audio files
AUDIO_DIR = "audio_files"
Path(AUDIO_DIR).mkdir(exist_ok=True)

# Set up Streamlit app
st.set_page_config(page_title="Text to Speech Converter", layout="wide")

# Inject custom CSS for main page styling only
st.markdown(
    """
    <style>
    body {
        background-color: grey;
        color: white;
        font-size: bold;
    }
    .stTextArea textarea {
        background-color: black;
        color: white;
        border: 1px solid white;
    }
    .stTextArea textarea:focus {
        border-color: red;
    }
    .stButton button {
        background-color: black;
        color: white;
        border: 1px solid white;
    }
    .stButton button:hover {
        background-color: red;
        color: white;
    }
    .stAudio, .stExpander {
        background-color: #333333; /* Dark gray for better contrast */
        color: white;
    }
    .stExpander:hover {
        background-color: #333333;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and instructions
import streamlit as st

# Display the title with HTML using markdown
import streamlit as st

# Display the title with the icons inline
# st.markdown(
#     """
#     <h1>Text <img src="./images/document-svgrepo-com.svg" style="width:30px;vertical-align:middle;"> to Speech <img src="./images/headphones-music-svgrepo-com.svg" style="width:30px;vertical-align:middle;"> Converter</h1>
#     """,
#     unsafe_allow_html=True
# )

st.title("Text 📝 to Speech 🗣️ Converter !")

# Sidebar for managing audio files (default Streamlit theme)
st.sidebar.title("Audio History")

# Function to clean up old audio files
def manage_audio_files(directory, max_files=15):
    files = sorted(Path(directory).iterdir(), key=os.path.getctime, reverse=True)
    if len(files) > max_files:
        for file in files[max_files:]:
            os.remove(file)

# Display audio files in the sidebar with delete functionality
manage_audio_files(AUDIO_DIR)
audio_files = sorted(Path(AUDIO_DIR).iterdir(), key=os.path.getctime, reverse=True)
if audio_files:
    st.sidebar.subheader("Saved Audio Files")
    for audio_file in audio_files:
        file_name = audio_file.stem  # File name without extension
        
        # Create collapsible menu for each audio file
        with st.sidebar.expander(file_name):
            st.audio(str(audio_file), format="audio/mp3")
            if st.button(f"Delete {file_name}", key=f"delete_{file_name}"):
                os.remove(audio_file)
                st.experimental_rerun()
else:
    st.sidebar.write("No audio files yet.")

# Main page: Text input
text_to_convert = st.text_area("Enter Text Here", height=200)

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Adjust settings (optional)
engine.setProperty("rate", 150)  # Speed of speech
engine.setProperty("volume", 1)  # Volume (0.0 to 1.0)

# Single button to handle Convert, Play, and Save
if st.button("Convert, Play, and Save"):
    if text_to_convert.strip():
        # Generate a filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = Path(AUDIO_DIR) / f"speech_{timestamp}.mp3"
        
        # Save the speech to a file
        engine.save_to_file(text_to_convert, str(file_path))
        engine.runAndWait()  # Only runs for saving to file, no live playback

        # Notify the user
        st.success(f"Audio converted and saved as {file_path.name}!")
        
        # Play the saved file using Streamlit's audio player
        st.audio(str(file_path), format="audio/mp3")

        # Manage audio files to retain only the last 15
        manage_audio_files(AUDIO_DIR)
    else:
        st.error("Please enter some text to convert.")

# Footer
st.markdown(
    "<small>Built with ❤️ using Streamlit</small>", 
    unsafe_allow_html=True
)