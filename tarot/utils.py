
import random
import requests
import openai
from django.conf import settings
from .llm.system_prompts import interpreter_prompt

openai.api_key = settings.OPENAI_API_KEY

TEMPLATE_DISPATCH = {
    "past_present_future": "tarot/past_present_future.html",
    "safe_passage": "tarot/lilias_safe_passage.html",
}


def generate_interpretation(cards, name, question):
    """Use OpenAI to generate a friendly tarot reading interpretation."""
    prompt = f"""
    {interpreter_prompt}
    Tarot reading for {name}.
    Question: {question}.
    Cards drawn:
    Past: {cards[0]['name']} {'(reversed)' if cards[0]['reversed'] else ''}
    Present: {cards[1]['name']} {'(reversed)' if cards[1]['reversed'] else ''}
    Future: {cards[2]['name']} {'(reversed)' if cards[2]['reversed'] else ''}

    Provide a concise, friendly interpretation of this reading.
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content

