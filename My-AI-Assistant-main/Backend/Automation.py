from AppOpener import close, open as appopen  
from webbrowser import open as webopen 
from pywhatkit import search, playonyt 
from dotenv import dotenv_values 
from bs4 import BeautifulSoup 
from rich import print  
from groq import Groq
import webbrowser 
import subprocess
import requests  
import keyboard 
import asyncio  
import os
import platform
import ctypes


env_vars = dotenv_values('.env')
GroqAPIKey = env_vars.get('GroqAPIKey')  


classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", 
           "IZ6rdc", "OSurRd LTKOO", "vLZv6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", 
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]


useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'


client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask."
]

messages = []

SystemChatBot = [{'role': 'system', 'content': f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic)  # Use the search function to perform a Google search.
    return True  # Indicate success of the search.
# GoogleSearch("Robert Downey Junior")

# Function to generate content using AI and save it to a file.
def Content(Topic):
    # नेस्टेड फंक्शन नोटपैड में फाइल ओपन करने के लिए
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    # नेस्टेड फंक्शन AI से कंटेंट जनरेट करने के लिए
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    # कंटेंट फोल्डर पाथ बनाएं
    content_dir = os.path.join("Data", "Content")
    os.makedirs(content_dir, exist_ok=True)  # फोल्डर न होने पर बनाएगा

    # फाइल पाथ बनाना
    filename = f"{Topic.lower().replace(' ', '')}.txt"
    file_path = os.path.join(content_dir, filename)

    # जनरेटेड कंटेंट सेव करना
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(file_path)  # अपडेटेड पाथ के साथ ओपन करना
    return True
# Content("write random poem")

# Function to search for a topic on YouTube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube search URL.
    webbrowser.open(Url4Search)  # Open the search URL in a web browser.
    return True  # Indicate success.
# YouTubeSearch("How to make jarvis AI")

# Function to play a video on YouTube.
def PlayYouTube(query):
    playonyt(query)  # Use pywhatkit's playonyt function to play the video.
    return True  # Indicate success.
# PlayYouTube("Main hoon saath tere")

# Function to open an application or a relevant webpage.
def OpenApp(app, sess=requests.session()):
    try:
        # Attempt to open the app locally.
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True  # Indicate success.
    except Exception as e:
        print(f"Error opening app locally: {e}")

    # If app cannot be found locally, construct the URL and open it.
    try:
        query = f"{app}"  # Use the app name as the query.
        url = f"https://www.{query}.com"  # Create the URL in the desired format.
        
        # Open the constructed URL.
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error opening the webpage: {e}")
        # print(f"But Trying to find the website...")
        return False
# OpenApp("Setting")

# Function to close an application.
def CloseApp(app):
    if "chrome" in app:
        pass  # Skip if the app is Chrome.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app.
            return True  # Indicate success.
        except:
            return False  # Indicate failure.
# CloseApp("settings")

# Function to execute system-level commands.
def System(command):
    # Volume control functions
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    # Media control functions
    def play_pause():
        keyboard.press_and_release("play/pause")

    def next_track():
        keyboard.press_and_release("next track")

    def previous_track():
        keyboard.press_and_release("previous track")

    # Screenshot function
    def take_screenshot():
        keyboard.press_and_release("print screen")

    # Brightness control functions (may not work on all systems)
    def brightness_up():
        keyboard.press_and_release("brightness up")

    def brightness_down():
        keyboard.press_and_release("brightness down")

    # System command functions
    def shutdown():
        system = platform.system()
        if system == "Windows":
            os.system("shutdown /s /t 1")
        elif system == "Linux":
            os.system("systemctl poweroff")
        elif system == "Darwin":
            os.system("osascript -e 'tell app \"System Events\" to shut down'")

    def restart():
        system = platform.system()
        if system == "Windows":
            os.system("shutdown /r /t 1")
        elif system == "Linux":
            os.system("systemctl reboot")
        elif system == "Darwin":
            os.system("osascript -e 'tell app \"System Events\" to restart'")

    def lock_system():
        system = platform.system()
        if system == "Windows":
            ctypes.windll.user32.LockWorkStation()
        elif system == "Linux":
            os.system("gnome-screensaver-command -l")
        elif system == "Darwin":
            os.system("/System/Library/CoreServices/Menu/Extras/User.menu/Contents/Resources/CGSession -suspend")

    # Mapping of commands to their respective functions
    command_handlers = {
        "mute": mute,
        "unmute": unmute,
        "volume up": volume_up,
        "volume down": volume_down,
        "play/pause": play_pause,
        "next track": next_track,
        "previous track": previous_track,
        "screenshot": take_screenshot,
        "brightness up": brightness_up,
        "brightness down": brightness_down,
        "shutdown": shutdown,
        "restart": restart,
        "lock the system": lock_system,
    }

    # Retrieve the appropriate handler
    handler = command_handlers.get(command)

    if handler:
        try:
            handler()
            return True
        except Exception as e:
            print(f"Error executing command '{command}': {e}")
            return False
    else:
        return False  # Command not recognized
# System("lock the system")

# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):

    funcs = []  # List to store asynchronous tasks.

    for command in commands:

        if command.startswith("open "):  # Handle "open" commands.

            if "open it" in command:  # Ignore "open it" commands.
                pass

            if "open file" == command:  # Ignore "open file" commands.
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  # Schedule app opening.
                funcs.append(fun)

        elif command.startswith("general "):  # Placeholder for general commands.
            pass

        elif command.startswith("realtime "):  # Placeholder for real-time commands.
            pass

        elif command.startswith("close "):  # Handle "close" commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))  # Schedule app closing.
            funcs.append(fun)

        elif command.startswith("play "):  # Handle "play" commands.
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))  # Schedule YouTube playback.
            funcs.append(fun)

        elif command.startswith("content "):  # Handle "content" commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content "))  # Schedule content creation.
            funcs.append(fun)

        elif command.startswith("google search "):  # Handle Google search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))  # Schedule Google search.
            funcs.append(fun)

        elif command.startswith("youtube search "):  # Handle YouTube search commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))  # Schedule YouTube search.
            funcs.append(fun)

        elif command.startswith("system "):  # Handle system commands.
            fun = asyncio.to_thread(System, command.removeprefix("system "))  # Schedule system command.
            funcs.append(fun)
        else:
            print(f"No Function Found. For {command}")  # Print an error for unrecognized commands.

    results = await asyncio.gather(*funcs)  # Execute all tasks concurrently.

    for result in results:  # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):  # Translate and execute commands.
        pass

    return True  # Indicate success.


# if __name__ == "__main__":
#     asyncio.run(Automation(["open facebook", "open firefox", "open settings", "play senorita"]))

