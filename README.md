# Star_Bot

# StarBot: AI Voice Assistant

StarBot is a Python-based virtual assistant designed to help users perform a variety of tasks through voice commands. It leverages speech recognition, text-to-speech capabilities, and web browsing to deliver a voice-enabled experience similar to Alexa or Google Assistant. StarBot can perform web searches, set alarms, provide date and time information, convert units, and much more.

---

## Features

- **Voice Recognition**: Listens to voice commands and converts them to text.
- **Text-to-Speech**: Responds with voice, providing a conversational experience.
- **Wikipedia Search**: Retrieves summaries of topics from Wikipedia.
- **Web Browsing**: Opens YouTube, Google, and performs Google searches on specific terms.
- **Date and Time**: Provides the current date and time on request.
- **Alarm and Timer**: Sets alarms and timers as specified by the user.
- **Unit Conversion**: Converts between various units of measurement, including length, weight, volume, and temperature.
- **Customizable UI**: Optional Tkinter-based GUI allows text-based interaction and displays conversation history.

---

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/StarBot.git
    ```
2. **Navigate to the project directory**:
    ```bash
    cd StarBot
    ```
3. **Install dependencies**:
    ```bash
    pip install pyttsx3 speechrecognition wikipedia
    ```
4. **Run the application**:
    ```bash
    python StarBot.py
    ```

---

## Usage

1. **Launch**: Start the program to initiate StarBot.
2. **Commands**: Speak commands like "What is the date today?", "Open YouTube", "Convert 5 kilometers to miles", etc.
3. **Exit**: Say "Quit", "Exit", or "Go to sleep" to end the session.

---

## Implementation Details

### Modules

- **pyttsx3**: Provides text-to-speech functionality for StarBot's voice responses.
- **speech_recognition**: Detects and interprets user speech through microphone input.
- **datetime**: Retrieves the current date and time for responding to related queries.
- **wikipedia**: Allows StarBot to fetch information on topics from Wikipedia.
- **webbrowser**: Enables StarBot to open specific URLs, such as YouTube or Google, in the user's default browser.
- **re**: Handles regular expressions for parsing text commands, especially in unit conversions.
- **time**: Facilitates the timer and alarm functionalities by managing time intervals.
- **tkinter**: Used optionally for a GUI interface that displays a conversation history and input box.

### Key Functions

- `speak(audio)`: Converts text to speech, allowing StarBot to respond audibly.
- `wishMe()`: Greets the user based on the time of day.
- `takeCommand()`: Captures and transcribes user voice input.
- `tell_date()`: Provides the current date.
- `set_alarm(alarm_time)`: Sets an alarm for the specified time in HH:MM format.
- `set_timer(timer_minutes)`: Sets a timer for a specified number of minutes.
- `convert_units(value, from_unit, to_unit)`: Converts between various units of length, weight, volume, and temperature.
- `command_handler(query)`: Main function for parsing user commands and invoking the appropriate function.

---

### GUI (Optional)

The optional GUI uses Tkinter, providing a scrollable chat window that displays the conversation history. It includes buttons for sending text input, initiating voice commands, and displaying StarBot's responses.

- **Chat Window**: Displays both user queries and StarBot's responses.
- **Input Box**: Allows users to enter text commands manually.
- **Voice Input Button**: Activates voice input mode.
- **Send Button**: Sends text input from the input box.

---
