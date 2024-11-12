import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import re
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    print(f"StarBot: {audio}")  # Display what the application is going to speak
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("This is StarBot, your AI companion. How can I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        print(f"User: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Sorry, there seems to be a network issue.")
        return None

def tell_date():
    today_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {today_date}.")

def set_alarm(alarm_time):
    try:
        speak(f"Setting alarm for {alarm_time}")
        alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
        while True:
            current_time = datetime.datetime.now()
            if current_time.hour == alarm_hour and current_time.minute == alarm_minute:
                speak("Wake up! It's time.")
                break
            time.sleep(60)
    except ValueError:
        speak("Invalid time format. Please specify time in HH:MM format.")

def set_timer(timer_minutes):
    try:
        speak(f"Setting timer for {timer_minutes} minutes")
        timer_seconds = int(timer_minutes) * 60
        time.sleep(timer_seconds)
        speak(f"The timer for {timer_minutes} minutes is up!")
    except ValueError:
        speak("Invalid timer value.")

def convert_units(value, from_unit, to_unit):
    """Converts between specified units."""
    conversion_table = {
        'length': {
            'meters': {
                'kilometers': lambda x: x / 1000,
                'feet': lambda x: x * 3.28084,
                'inches': lambda x: x * 39.3701,
                'centimeters': lambda x: x * 100,
                'miles': lambda x: x / 1609.34,
                'yards': lambda x: x * 1.09361,
                'millimeters': lambda x: x * 1000,
            },
            'kilometers': {
                'meters': lambda x: x * 1000,
                'feet': lambda x: x * 3280.84,
                'inches': lambda x: x * 39370.1,
                'centimeters': lambda x: x * 100000,
                'miles': lambda x: x / 1.60934,
                'yards': lambda x: x * 1093.61,
                'millimeters': lambda x: x * 1000000,
            },
            'feet': {
                'meters': lambda x: x / 3.28084,
                'kilometers': lambda x: x / 3280.84,
                'inches': lambda x: x * 12,
                'centimeters': lambda x: x * 30.48,
                'miles': lambda x: x / 5280,
                'yards': lambda x: x / 3,
                'millimeters': lambda x: x * 304.8,
            },
            'inches': {
                'meters': lambda x: x / 39.3701,
                'kilometers': lambda x: x / 39370.1,
                'feet': lambda x: x / 12,
                'centimeters': lambda x: x * 2.54,
                'miles': lambda x: x / 63360,
                'yards': lambda x: x / 36,
                'millimeters': lambda x: x * 25.4,
            },
            'centimeters': {
                'meters': lambda x: x / 100,
                'kilometers': lambda x: x / 100000,
                'feet': lambda x: x / 30.48,
                'inches': lambda x: x / 2.54,
                'miles': lambda x: x / 160934,
                'yards': lambda x: x / 91.44,
                'millimeters': lambda x: x * 10,
            },
            'millimeters': {
                'meters': lambda x: x / 1000,
                'kilometers': lambda x: x / 1000000,
                'feet': lambda x: x / 304.8,
                'inches': lambda x: x / 25.4,
                'miles': lambda x: x / 1.609e+6,
                'yards': lambda x: x / 914.4,
                'centimeters': lambda x: x / 10,
            },
            'miles': {
                'meters': lambda x: x * 1609.34,
                'kilometers': lambda x: x * 1.60934,
                'feet': lambda x: x * 5280,
                'inches': lambda x: x * 63360,
                'yards': lambda x: x * 1760,
                'centimeters': lambda x: x * 160934,
                'millimeters': lambda x: x * 1.609e+6,
            },
            'yards': {
                'meters': lambda x: x / 1.09361,
                'kilometers': lambda x: x / 1093.61,
                'feet': lambda x: x * 3,
                'inches': lambda x: x * 36,
                'miles': lambda x: x / 1760,
                'centimeters': lambda x: x * 91.44,
                'millimeters': lambda x: x * 914.4,
            }
        },
        'weight': {
            'grams': {
                'kilograms': lambda x: x / 1000,
                'pounds': lambda x: x * 0.00220462,
                'ounces': lambda x: x * 0.035274,
            },
            'kilograms': {
                'grams': lambda x: x * 1000,
                'pounds': lambda x: x * 2.20462,
                'ounces': lambda x: x * 35.274,
            },
            'pounds': {
                'grams': lambda x: x / 0.00220462,
                'kilograms': lambda x: x / 2.20462,
                'ounces': lambda x: x * 16,
            },
            'ounces': {
                'grams': lambda x: x / 0.035274,
                'kilograms': lambda x: x / 35.274,
                'pounds': lambda x: x / 16,
            }
        },
        'volume': {
            'liters': {
                'milliliters': lambda x: x * 1000,
                'gallons': lambda x: x * 0.264172,
                'quarts': lambda x: x * 1.05669,
            },
            'milliliters': {
                'liters': lambda x: x / 1000,
                'gallons': lambda x: x * 0.000264172,
                'quarts': lambda x: x * 0.00105669,
            },
            'gallons': {
                'liters': lambda x: x / 0.264172,
                'milliliters': lambda x: x / 0.000264172,
                'quarts': lambda x: x * 4,
            },
            'quarts': {
                'liters': lambda x: x / 1.05669,
                'milliliters': lambda x: x / 0.00105669,
                'gallons': lambda x: x * 0.25,
            }
        },
        'temperature': {
            'celsius': {
                'fahrenheit': lambda x: (x * 9/5) + 32,
                'kelvin': lambda x: x + 273.15,
            },
            'fahrenheit': {
                'celsius': lambda x: (x - 32) * 5/9,
                'kelvin': lambda x: (x - 32) * 5/9 + 273.15,
            },
            'kelvin': {
                'celsius': lambda x: x - 273.15,
                'fahrenheit': lambda x: (x - 273.15) * 9/5 + 32,
            }
        }
    }

    # Determine the category of conversion
    category = None
    for cat, units in conversion_table.items():
        if from_unit in units and to_unit in units[from_unit]:
            category = cat
            break

    if category:
        try:
            result = conversion_table[category][from_unit][to_unit](value)
            return result
        except KeyError:
            speak("Sorry, I couldn't perform the conversion. Please check the units.")
            return None
    else:
        speak("Sorry, I couldn't perform the conversion. Please check the units.")
        return None

def command_handler(query):
    if query is None:
        return

    if 'wikipedia' in query:
        try:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError:
            speak("The term is too ambiguous, please specify your query.")
        except wikipedia.exceptions.PageError:
            speak("No page found on Wikipedia.")

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")

    elif 'open google' in query:
        webbrowser.open("google.com")

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {strTime}")

    elif 'weather' in query:
        speak('Please specify your location.')
        location = takeCommand()
        if location:
            url = f"https://www.google.com/search?q=weather+in+{location}"
            webbrowser.get().open(url)
            speak(f"Here's the weather in {location}.")
        else:
            speak("I couldn't fetch the location.")

    elif 'how are you' in query:
        speak("I am fine. How about you?")

    elif 'i am good' in query or 'i am well' in query:
        speak("Great!")

    elif 'set alarm' in query:
        speak("At what time should I set the alarm? Please specify in HH:MM format.")
        alarm_time = takeCommand()
        if alarm_time:
            set_alarm(alarm_time)

    elif 'set timer' in query:
        speak("For how many minutes should I set the timer?")
        timer_minutes = takeCommand()
        if timer_minutes:
            set_timer(timer_minutes)

    elif 'convert' in query:
        conversion = re.search(r'(\d+)\s*(\w+)\s+to\s+(\w+)', query)
        if conversion:
            value, from_unit, to_unit = conversion.groups()
            # Normalize units for consistent matching

            from_unit = from_unit.lower()
            to_unit = to_unit.lower()
            result = convert_units(float(value), from_unit, to_unit)
            if result is not None:
                speak(f"{value} {from_unit} is equal to {result:.2f} {to_unit}.")
        else:
            speak("Sorry, I couldn't understand the conversion request.")

    elif 'search for' in query or 'search' in query:
        person_name = query.replace('search for', '').strip()
        if person_name:
            speak(f"Searching for {person_name} on Google.")
            webbrowser.open(f"https://www.google.com/search?q={person_name}")
        else:
            speak("Please specify the name of the person to search.")

    elif 'date' in query:
        tell_date()

    elif 'quit' in query or 'exit' in query or 'go to sleep' in query:
        speak("Goodbye!")
        exit(0)

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()
        command_handler(query)

###########################         Basic UI for the application using tkinter    ############################

# import pyttsx3
# import speech_recognition as sr
# import datetime
# import wikipedia
# import webbrowser
# import re
# import time
# import tkinter as tk
# from tkinter import scrolledtext

# # Initialize the text-to-speech engine
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

# # Function to speak text
# def speak(audio):
#     chat_window.insert(tk.END, f"StarBot: {audio}\n")
#     engine.say(audio)
#     engine.runAndWait()

# # Wish the user
# def wishMe():
#     hour = int(datetime.datetime.now().hour)
#     if hour >= 0 and hour < 12:
#         speak("Good morning!")
#     elif hour >= 12 and hour < 18:
#         speak("Good afternoon!")
#     else:
#         speak("Good evening!")
#     speak("This is StarBot, your AI companion. How can I help you?")

# # Take voice command from the microphone
# def take_voice_command():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source, duration=1)
#         speak("Listening...")
#         try:
#             audio = r.listen(source, timeout=5)
#             query = r.recognize_google(audio)
#             chat_window.insert(tk.END, f"User: {query}\n")
#             command_handler(query.lower())
#         except sr.UnknownValueError:
#             speak("Sorry, I did not understand that.")
#         except sr.RequestError:
#             speak("Sorry, there seems to be a network issue.")
#         except sr.WaitTimeoutError:
#             speak("No voice detected, please try again.")

# # Command handler for input
# def command_handler(query):
#     if query is None:
#         return

#     if 'wikipedia' in query:
#         try:
#             speak('Searching Wikipedia...')
#             query = query.replace("wikipedia", "")
#             results = wikipedia.summary(query, sentences=2)
#             speak("According to Wikipedia")
#             speak(results)
#         except wikipedia.exceptions.DisambiguationError:
#             speak("The term is too ambiguous, please specify your query.")
#         except wikipedia.exceptions.PageError:
#             speak("No page found on Wikipedia.")

#     elif 'open youtube' in query:
#         webbrowser.open("youtube.com")
#         speak("Opening YouTube")

#     elif 'open google' in query:
#         webbrowser.open("google.com")
#         speak("Opening Google")

#     elif 'the time' in query:
#         strTime = datetime.datetime.now().strftime("%H:%M")
#         speak(f"The time is {strTime}")

#     elif 'search for' in query:
#         person_name = query.replace('search for', '').strip()
#         if person_name:
#             speak(f"Searching for {person_name} on Google.")
#             webbrowser.open(f"https://www.google.com/search?q={person_name}")

#     elif 'date' in query:
#         tell_date()

#     elif 'quit' in query or 'exit' in query:
#         speak("Goodbye!")
#         window.quit()

# # Function to tell the current date
# def tell_date():
#     today_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
#     speak(f"Today's date is {today_date}.")

# # Get user input from the textbox
# def send_message():
#     query = input_box.get()
#     input_box.delete(0, tk.END)
#     chat_window.insert(tk.END, f"User: {query}\n")
#     command_handler(query.lower())

# # UI Design with Tkinter
# window = tk.Tk()
# window.title("StarBot AI Companion")

# # Chat window (scrollable)
# chat_window = scrolledtext.ScrolledText(window, width=50, height=20, state='normal', wrap='word')
# chat_window.grid(row=0, column=0, columnspan=3)
# chat_window.config(state='normal')

# # Input box
# input_box = tk.Entry(window, width=40)
# input_box.grid(row=1, column=0)

# # Send button for text input
# send_button = tk.Button(window, text="Send", command=send_message)
# send_button.grid(row=1, column=1)

# # Voice input button
# voice_button = tk.Button(window, text="🎤 Voice Input", command=take_voice_command)
# voice_button.grid(row=1, column=2)

# # Trigger the initial greeting
# wishMe()

# # Start the Tkinter event loop
# window.mainloop()
