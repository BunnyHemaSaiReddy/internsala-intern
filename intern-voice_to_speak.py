import streamlit as st
import speech_recognition as sr
import gtts
import googletrans as gt
import io

def speak():
    """
    Captures speech input and converts it to text using Google Speech Recognition.
    """
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
        st.info("Listening... Speak now!")
        try:
            sound = rec.listen(mic, timeout=5, phrase_time_limit=10)
            text_rec = rec.recognize_google(sound)
            return text_rec
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError:
            st.error("Error connecting to Google Speech Recognition service.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
        return ""

def translate_text(text, to_lang, from_lang='en'):
    """
    Translates text from the source language to the target language using googletrans.
    """
    translator = gt.Translator()
    try:
        translated_text = translator.translate(text, src=from_lang, dest=to_lang)
        return translated_text.text
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return text

def play_audio(text, lang_code):
    """
    Converts text to audio using gTTS and plays it in Streamlit.
    """
    try:
        gtts_audio = gtts.gTTS(text, lang=lang_code)
        audio_buffer = io.BytesIO()
        gtts_audio.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        st.audio(audio_buffer, format="audio/mp3")
    except Exception as e:
        st.error(f"Audio generation failed: {e}")

def get_language_codes():
    """
    Returns a dictionary of language names and their corresponding codes.
    """
    return {name.capitalize(): code for code, name in gt.LANGUAGES.items()}

# Streamlit App Interface
st.title("Speech-to-Text Translator with Audio")
st.markdown("### 🗣️ Speak, Translate, and Listen")

language_codes = get_language_codes()
target_language = st.selectbox("Select the language for translation:", ["English"] + list(language_codes.keys()))

if st.button("Speak and Translate"):
    st.info("Preparing to capture your voice...")
    text = speak()
    
    if text:
        st.write("**You said:**", text)
        
        # Determine target language code
        lang_code = 'en'  # Default to English
        if target_language != "English":
            lang_code = language_codes.get(target_language.capitalize(), 'en')
        
        # Translate text if needed
        if lang_code != 'en':
            translated_text = translate_text(text, lang_code)
            st.write(f"**Translated Text ({target_language}):**", translated_text)
        else:
            translated_text = text
        
        # Play translated or original text as audio
        play_audio(translated_text, lang_code)
