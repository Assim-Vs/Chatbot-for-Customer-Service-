# app/chatbot.py

import random

faq_responses = {
    "plans": "We offer Basic, Standard and Premium plans. Which kind of service do you need?",
    "premium": "Our Premium plan offers HD streaming on 4 devices simultaneously.",
    "standard": "Our Standard plan offers HD streaming on 2 devices simultaneously.",
    "basic": "Our Basic plan offers SD streaming on 1 device.",
    "price": "Our plans start at ₹199 per month. You can upgrade or downgrade anytime.",
    "payment": "You can pay via UPI, card, or netbanking. Auto-debit is also available.",
    "cancel": "You can cancel your plan from account settings or I can connect you to support."
}

def get_response(user_input: str) -> str:
    text = user_input.lower().strip()

    # Greetings
    if any(g in text for g in ["hi", "hello", "hey"]):
        return random.choice([
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?"
        ])

    # Help
    if "help" in text:
        return "Sure! Are you asking about plans, price, payment, or cancellation?"

    # Simple weather rule (just for fun)
    if "weather" in text or "whether" in text:
        return "I'm mainly a customer service bot, but I think it's a great day to learn Python 😄"

    # FAQ keywords
    for key, resp in faq_responses.items():
        if key in text:
            return resp

    # Churn / leave / cancel hints
    if any(w in text for w in ["churn", "leave", "quit service"]):
        return "I can help you with retention offers or connect you to an agent to discuss your plan."

    # Fallback
    return "Sorry, I didn't get that. Do you want to ask about plans, price, payment, or cancellation?"
