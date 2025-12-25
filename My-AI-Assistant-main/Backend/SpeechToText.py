from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
# Get the input language setting from environment variables.
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code for the speech recognition interface.
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with input language environment variable.
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to this file.
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# Get the current working directory.
current_dir = os.getcwd()
# Generate the file path for HTML file.
Link = f"{current_dir}/Data/Voice.html"

# Set Chrome options for the webDriver.
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")
# # Disable unnecessary features to improve performance.
# chrome_options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns,UseChromeOSDirectVideoDecoder")
# chrome_options.add_argument("--disable-background-networking")
# chrome_options.add_argument("--disable-sync")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")

# Initialize the Chrome WebDriver using the ChromeDriverManager.
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the path for temporary files.
TempDirPath = rf"{current_dir}/Frontend/Files"

# Function to set the assistant's status by writing it to a file.
def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting.
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's", "can you"]

    # Check if the query is question and add a question mark if necessary.
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        # Add a period if the query is not a question.
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

# Function to translate text into English using the mtranslate library.
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to perform speech recognition using the WebDriver.
def SpeechRecognition():
    #open HTMLfile in browser.
    driver.get("file://" + Link)
    # Start speech recognition by clicking the start button.
    driver.find_element(by=By.ID, value="start").click()

    while True:
        try:
            # Get the recognized text from HTML output element.
            Text = driver.find_element(by=By.ID, value="output").text

            if Text:
                # Stop recognition by clicking stop button.
                driver.find_element(by=By.ID, value="end").click()

                # If inputed language is English.
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    # If the input language is English, translate the text and return it.
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        
        except Exception as e:
            pass

# Main execution block.
if __name__ == "__main__":
    while True:
        # Continuously perform speech recognition and print the text.
        Text = SpeechRecognition()
        print(Text)
        
