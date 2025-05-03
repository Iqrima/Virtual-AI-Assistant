# Nova - Voice Assistant

Nova is a sophisticated voice assistant built in Python that combines speech recognition, text-to-speech, and AI capabilities using Google's Gemini model. It features a graphical user interface built with PyQt5 for displaying outputs.

## Features

- Voice command recognition with wake word "Nova"
- News fetching and reading capabilities
- Music playback functionality
- Web browser integration (YouTube, Google, LinkedIn, Instagram)
- AI-powered conversations using Google's Gemini
- Noise reduction for better voice recognition
- GUI interface for output display

## Prerequisites

Before installing Nova, ensure you have the following:

- Python 3.8 or higher installed
- A working microphone for voice input
- Speakers or headphones for audio output
- Internet connection for AI and news features
- Windows, macOS, or Linux operating system

## Project Structure

```
nova/
│
├── main.py              # Main application entry point
├── music_library.py     # Music handling functionality
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Requirements

```
speech_recognition
pyttsx3
webbrowser
noisereduce
numpy
requests
google-generativeai
PyQt5
```

## Detailed Setup Guide

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nova-assistant.git
   cd nova-assistant
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys**
   - Create a `settings.json` file in the project root (this will be gitignored)
   ```json
   {
       "GEMINI_API_KEY": "your_gemini_api_key",
       "NEWS_API_KEY": "your_news_api_key"
   }
   ```
   - Get your API keys from:
     - Gemini API: [Google AI Studio](https://makersuite.google.com/app/apikey)
     - News API: [NewsAPI.org](https://newsapi.org/)

## Detailed Usage Guide

1. **Starting Nova**
   - Run `main.py` using Python:
     ```bash
     python main.py
     ```
   - The GUI window will appear showing "Initializing Nova..."
   - Wait for the initialization to complete

2. **Voice Commands**
   - Say "Nova" to activate the assistant
   - Wait for the activation sound
   - Speak your command clearly
   - Commands are case-insensitive

3. **Available Commands in Detail**
   - **News Related**
     - "Give me news" - Fetches and reads latest business news
     - "News about [topic]" - Fetches news about specific topic
   
   - **Web Navigation**
     - "Open YouTube" - Opens YouTube in default browser
     - "Open Google" - Opens Google search
     - "Open LinkedIn" - Opens LinkedIn homepage
     - "Open Instagram" - Opens Instagram website
   
   - **Music Controls**
     - "Play music" - Prompts for track selection
     - "List music" - Shows available music tracks
     - "Stop music" - Stops current playback
     - "Next song" - Plays next track
     - "Previous song" - Plays previous track
   
   - **System Commands**
     - "Exit" - Closes the application
     - "Help" - Lists available commands
     - "Volume up/down" - Adjusts system volume

4. **AI Conversation**
   - Any input not matching predefined commands will be processed by Gemini AI
   - The AI can engage in conversations, answer questions, and provide assistance
   - Responses are both spoken and displayed in the GUI

## Troubleshooting

Common issues and solutions:

1. **Microphone not working**
   - Check if microphone is properly connected
   - Verify microphone permissions in system settings
   - Try selecting a different audio input device

2. **API Key Issues**
   - Verify API keys are correctly formatted in settings.json
   - Check if API keys are valid and not expired
   - Ensure proper internet connectivity

3. **Audio Output Problems**
   - Check system volume settings
   - Verify default audio output device
   - Restart the application

## Performance Optimization

- Use a noise-canceling microphone for better voice recognition
- Close background applications to improve performance
- Consider upgrading Python to the latest version for better compatibility
- Use a wired internet connection for more reliable API responses

## Security Note

⚠️ Make sure to keep your API keys secure and never commit them directly to the repository.

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Run tests if available
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

## License

MIT License - feel free to use this code for your own projects.

## Version History

- v1.0.0 (Initial Release)
  - Basic voice command functionality
  - News and music integration
  - Web browser controls
  - AI conversation capabilities