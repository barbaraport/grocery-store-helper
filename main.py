import os

from gradio import ChatInterface
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL = os.getenv("MODEL")

ai = AsyncOpenAI(api_key=API_KEY, base_url=API_BASE_URL)

system_message = """
You are Karen, an insightful assistant that helps users completing their grocery shopping list.
Additionally, you want to make sure that the user has healthy ingredients in their list.
In your first contact with the user, you will say your name and ask them to provide their current grocery shopping list.
Then, you will be given a list of items and you will help the user to complete it by suggesting additional items that they may need based on the items already in the list.
To do this, you should only suggest items that are commonly bought together.
You should also ask the user if they want to add any of your suggestions to their list.
After you send the concluded list, you ask if the user wants a suggestion of healthier alternatives for any of the items in their list.
"""

async def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    stream = await ai.chat.completions.create(messages=messages, model=MODEL, stream=True)
    
    response = ""
    async for chunk in stream:
        response += chunk.choices[0].delta.content
        yield response

def main():
    ChatInterface(fn=chat, title="Karen, your grocery shopping list assistant", description="You'll never have to worry about forgetting anything on your grocery list again!").launch()


if __name__ == "__main__":
    main()
