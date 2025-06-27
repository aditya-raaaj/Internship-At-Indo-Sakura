import google.generativeai as genai
from datetime import datetime
import json

# Gemini API Key
GOOGLE_API_KEY = "AIzaSyCd6RHMfgyry-J7yhgYBN8m0RQkCWnugzA"

# Set up Gemini client
genai.configure(api_key=GOOGLE_API_KEY)

def chat_with_gemini(user_query, chat_history):
    """Fetch AI-generated responses using Gemini API with chat context"""
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Format prior chat history as prompt context
    full_prompt = ""
    for exchange in chat_history:
        full_prompt += f"You: {exchange['user']}\nBot: {exchange['bot']}\n"
    full_prompt += f"You: {user_query}\nBot:"

    response = model.generate_content(full_prompt)
    return response.text.strip()

def chatbot():
    """Real-time chatbot with memory & persistent history saving"""
    print("🤖 AI Chatbot Ready! Type 'exit' to stop.")
    chat_history = []

    while True:
        query = input("\nYou: ")
        if query.lower() == "exit":
            print("Goodbye! 👋")
            break

        reply = chat_with_gemini(query, chat_history)
        print(f"\nBot: {reply}")

        # Add new exchange with timestamp
        chat_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": query,
            "bot": reply
        })

        # Save updated chat history to file after each turn
        with open("chat_history.json", "w", encoding="utf-8") as file:
            json.dump(chat_history, file, indent=4)

# Run chatbot
chatbot()

