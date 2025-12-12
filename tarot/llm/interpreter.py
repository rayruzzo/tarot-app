from .system_prompts import interpreter_prompt
from ..models import LLMRequest, AIPrompt, Reading
from ..utils import handle_errors

@handle_errors
def create_interpretation_prompt(reading_id): 
    print(f"[create_interpretation_prompt] reading_id: {reading_id}")
    new_interpretation = AIPrompt(
        readingId=reading_id,
        systemPrompt=interpreter_prompt,
    )
    new_interpretation.save()
    print(f"[create_interpretation_prompt] Created and saved AIPrompt: {new_interpretation}")
    return new_interpretation

@handle_errors
def get_prompt(reading_id):
    prompt = AIPrompt.objects.get(readingId=reading_id)
    return prompt

@handle_errors
def generate_interpretation_prompt(reading_id):
    new_prompt = create_interpretation_prompt(reading_id)
    messages = new_prompt.create_messages()

    response = LLMRequest(messages=messages).make_request()

    return response

@handle_errors
def save_interpretation(reading_id, interpretation):
    reading = Reading.objects.get(id=reading_id)
    reading.interpretation = interpretation
    reading.save()
    return reading

@handle_errors
def get_interpretation(reading_id):
    reading = Reading.objects.get(id=reading_id)
    return reading.interpretation