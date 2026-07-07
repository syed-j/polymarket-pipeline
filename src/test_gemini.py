import os
from dotenv import load_dotenv
from google import genai

# load the key from your .env file (never hardcode it)
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ask Gemini a question
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="In one sentence, what is a prediction market?"
)

print(response.text)