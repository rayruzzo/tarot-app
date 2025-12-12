from .system_prompts import interpreter_prompt
from ..models import LLMRequest, AIPrompt, Reading
from ..utils import handle_errors

@handle_errors
def create_interpretation_prompt(reading_id): 
    new_interpretation = AIPrompt(
        reading_id=reading_id,
        system_prompt=interpreter_prompt,
    )
    new_interpretation.save()
    return new_interpretation

@handle_errors
def get_prompt(reading_id):
    prompt = AIPrompt.objects.get(reading_id=reading_id)
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