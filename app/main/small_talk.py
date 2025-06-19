import random
import re

def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower().strip())

def handle_small_talk(user_input):
    cleaned_input = normalize(user_input)

    greetings = {
        "hi", "hello", "hey", "good morning", "good afternoon", "good evening", 
        "greetings", "what's up", "howdy", "yo", "sup", "hi there", "hello there", "hey there", "hiya"
    }

    farewells = {
        "bye", "goodbye", "see you", "take care", "farewell", "later", "catch you later",
        "see you soon", "adios", "ciao", "peace out", "until next time", 
        "good night", "have a nice day", "have a great day", "have a good one", "take it easy"
    }

    thanks = {
        "thanks", "thank you", "thx", "thank you very much", "thanks a lot", "many thanks",
        "appreciate it", "much appreciated", "grateful", "cheers", "ta",
        "thank you kindly", "thank you so much", "thanks a bunch", "thanks a million"
    }

    bot_queries = {
        "who are you", "what are you", "what can you do", "your name", "what's your name",
        "who is your creator", "who made you", "who developed you", "what is your purpose",
        "what is your function", "what are you here for", "what can you assist with",
        "what can you help with", "what can you support with", "what are your capabilities",
        "what are your features"
    }

    help_queries = {
        "help me", "assist me", "support me", "can you help", "can you assist", "can you support",
        "how can you help", "how can you assist", "how can you support"
    }

    feeling_queries = {
        "how are you", "how's it going", "how do you do", "how are you doing", "how have you been",
        "how's everything", "how's life", "how's your day", "how's your week", "how's your month", "how's your year"
    }

    if cleaned_input in feeling_queries:
        return random.choice([
            "I'm just a bot, but I'm here to help you!",
            "I'm doing great, thanks for asking! How can I assist you today?",
            "I'm here and ready to help! What do you need?"
        ])

    if cleaned_input in greetings:
        return random.choice(["Hello!", "Hi there!", "Hey, how can I help you today?"])

    if cleaned_input in bot_queries:
        return "I'm a FinOps assistant bot here to help you with cloud related questions."

    if cleaned_input in help_queries:
        return "Sure! You can ask me about cloud cost management, budgeting, or any FinOps related topics."

    if cleaned_input in thanks:
        return random.choice(["You're welcome!", "No problem!", "Glad to help!"])

    if cleaned_input in farewells:
        return random.choice(["Goodbye!", "See you soon!", "Take care!"])

    return None
