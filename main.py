import speech_recognition as sr
import pyttsx3
import webbrowser
import noisereduce as nr
import numpy as np
import music_library
import requests
import google.generativeai as genai
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QObject, pyqtSignal
import sys
import io
from contextlib import redirect_stdout

class OutputRedirector(QObject):
    outputWritten = pyqtSignal(str)

    def write(self, text):
        self.outputWritten.emit(str(text))

    def flush(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova Assistant Output")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create text edit for output
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        # Redirect stdout to our custom handler
        self.redirector = OutputRedirector()
        self.redirector.outputWritten.connect(self.update_output)
        sys.stdout = self.redirector

    def update_output(self, text):
        self.output_text.append(text)
        self.output_text.verticalScrollBar().setValue(
            self.output_text.verticalScrollBar().maximum()
        )

# Create QApplication instance
app = QApplication(sys.argv)
window = MainWindow()
window.show()

# API Configuration
GEMINI_API_KEY = "AIzaSyC5131CZN9aF5VjdvX79EgkpsjJAD_r9ks"  # Replace with your Gemini API Key
genai.configure(api_key=GEMINI_API_KEY)

# List available models and select one.
available_models = list(genai.list_models())
if available_models:
    # Option 1: Use the first available model (dynamic)
    # valid_model_name = available_models[0].name

    # Option 2: Select a specific model by name (if you know it exists)
    valid_model_name = "models/gemini-2.0-flash"  # Added the model name here.

    # Option 3: Hard code the name (Not recommended, model names can change)
    # valid_model_name = "models/gemini-pro"  # Replace with desired Model.

    print(f"Using model: {valid_model_name}")
    gemini_model = genai.GenerativeModel(valid_model_name)  # Corrected line.
else:
    print("No Gemini models available.")
    exit()

API_KEY = "3f2acba03f87408eb76cfc6dcdb05a71"  # Replace with your News API Key
BASE_URL = "https://newsapi.org/v2/top-headlines"

# pyttsx3 initialization
engine = pyttsx3.init()
female_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty("voice", female_voice_id)

# Speech functions
def speak(text):
    engine.say(text)
    engine.runAndWait()

def reduce_noise(audio_data, sample_rate):
    reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=sample_rate)
    return reduced_noise_audio

# News fetching
def fetch_news(category="business", country="us"):
    try:
        params = {
            "apiKey": API_KEY,
            "category": category,
            "country": country,
            "q": country,
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        print(f"NewsAPI Response: {data}")

        if data["status"] == "ok" and data["totalResults"] > 0:
            articles = data.get("articles", [])
            return [article["title"] for article in articles[:5]]
        else:
            speak("No news available at the moment.")
            return ["No news available at the moment."]
    except Exception as e:
        return [f"An error occurred: {e}"]

def speak_news(category="business"):
    headlines = fetch_news(category=category)
    if headlines:
        speak(f"Here are the top {category} news headlines from us.")
        for idx, headline in enumerate(headlines, start=1):
            print(f"{idx}. {headline}")
            speak(headline)
    else:
        speak("Sorry, I couldn't fetch the news.")

# Command processing
def process_command(command):
    command = command.lower()
    print(f"Recognized command: {command}")

    if "give me news" in command or "show me news" in command or "news" in command:
        speak_news(category="business")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn.")
    elif "open instagram" in command:
        webbrowser.open("https://instagram.com")
        speak("Opening Instagram.")
    elif "play music" in command:
        speak("Which music do you want to play?")
        print("Available tracks:", ", ".join(music_library.music.keys()))
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                speak("Listening for the track name...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                track = recognizer.recognize_google(audio).lower()
                print(f"Recognized track: {track}")

                if track in music_library.music:
                    webbrowser.open(music_library.music[track])
                    speak(f"Playing {track}.")
                else:
                    speak("Sorry, that track is not available.")
        except sr.UnknownValueError:
            speak("I didn't catch the track name. Please try again.")
        except sr.RequestError as e:
            speak(f"There was an issue with the speech recognition service: {e}")
    elif "list music" in command:
        speak("Here are the available tracks:")
        for title in music_library.music.keys():
            print(f"- {title}")
        speak(", ".join(music_library.music.keys()))
    elif "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        try:
            response = gemini_model.generate_content(command)
            gemini_response_text = response.text
            print(f"Gemini response: {gemini_response_text}")
            speak(gemini_response_text)
        except Exception as e:
            speak("I'm unable to process that request right now.")
            print(f"An error occurred during Gemini processing: {e}")

# Main logic
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    speak("Initializing Nova...")
    while True:
        try:
            print("Waiting for wake word...")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)

                raw_data = audio.get_raw_data()
                sample_rate = audio.sample_rate
                reduced_audio = reduce_noise(np.frombuffer(raw_data, dtype=np.int16), sample_rate)
                reduced_audio_data = sr.AudioData(reduced_audio.tobytes(), sample_rate, audio.sample_width)

                word = recognizer.recognize_google(reduced_audio_data)
                print(f"Recognized wake word: {word}")

            if "nova" in word.lower():
                speak("Yes boss, I am here.")
                print("Listening for command...")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

                    raw_data = audio.get_raw_data()
                    reduced_audio = reduce_noise(np.frombuffer(raw_data, dtype=np.int16), sample_rate)
                    reduced_audio_data = sr.AudioData(reduced_audio.tobytes(), sample_rate, audio.sample_width)

                    command = recognizer.recognize_google(reduced_audio_data)
                    print(f"Recognized command: {command}")
                    process_command(command)

        except sr.UnknownValueError:
            print("Could not understand audio.")
            speak("I didn't catch that. Could you repeat?")
        except sr.RequestError as e:
            print(f"Error with the recognition service: {e}")
            speak("There was an error with the speech recognition service.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            speak("An unexpected error occurred. Please try again.")

sys.exit(app.exec_())