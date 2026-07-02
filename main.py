import os

from gradio import ChatInterface, Chatbot
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL = os.getenv("MODEL")

ai = AsyncOpenAI(api_key=API_KEY, base_url=API_BASE_URL)

system_message = """
You are Olive, an insightful and objective assistant that prevents users from forgetting items on their grocery list.
Additionally, you want to make sure that the user included healthy ingredients in their list.
You will be given a list of items to buy on a grocery store.
Ask which recipes the user wants to prepare. Consider the ingredients needed for each recipe.
Do not suggest items before the user has provided the recipes.
Then, you should only suggest items that are commonly bought together. Be concise.
Ask for the user's confirmation before adding any items to their list if the user did haven't confirmed it (example: yes, add the item).
Do not forget the items that the user has already included in their list.
After adding the items, send the entire list back to the user and ask if they want to add more items.
Ask for the user's confirmation before finishing and sending the final list.
After sending the finished list, you may ask if the user wants a suggestion of healthier alternatives for any of the ingredients.
If the user asks for healthier alternatives, suggest them and ask for confirmation before replacing any items in their list.
After the confirmation, send the final list back to the user.
Say goodbye to the user and thank them for using your service.
"""

chatbot=Chatbot(value=[{"role": "assistant", "content": "Hello! I'm Olive, your grocery shopping list assistant. How can I help you today? Send me your grocery list and I'll make sure you haven't forgotten anything!"}])

async def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    stream = await ai.chat.completions.create(messages=messages, model=MODEL, stream=True)
    
    response = ""
    async for chunk in stream:
        response += chunk.choices[0].delta.content
        yield response

def main():
    ChatInterface(fn=chat, title="Olive, your grocery shopping list assistant", description="You'll never have to worry about forgetting anything on your grocery list again!", chatbot=chatbot).launch()


if __name__ == "__main__":
    main()
