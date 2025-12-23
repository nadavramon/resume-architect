import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load the environment variables
load_dotenv()

# 2. Initialize the client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# 3. Send a test message
print("Sending request to Groq...")
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain what a Pub/Sub system is in one sentence.",
        }
    ],
    # UPDATED MODEL NAME HERE:
    model="llama-3.3-70b-versatile",
)

# 4. Print the result
print("\nResponse from Groq:")
print(chat_completion.choices[0].message.content)