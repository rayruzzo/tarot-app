from .system_prompts import interpreter_prompt
from ..models import LLMRequest, TarotInterpreter, Reading
from ..utils import handle_errors

@handle_errors
def create_interpreter(reading_id): 
    print(f"[create_interpreter] reading_id: {reading_id}")
    new_interpreter = TarotInterpreter(
        readingId=reading_id,
        systemPrompt=interpreter_prompt,
    )
    new_interpreter.save()
    print(f"[create_interpreter] Created and saved TarotInterpreter: {new_interpreter}")
    return {"TarotInterpreter": new_interpreter, "interpreterId": new_interpreter.id, "status": "success"}

@handle_errors
def get_interpreter(reading_id):
    interpreter = TarotInterpreter.objects.get(readingId=reading_id)
    return {"TarotInterpreter": interpreter, "status": "success"}

@handle_errors
def generate_interpretation(interpreter_id):
    try:
        interpreter = TarotInterpreter.objects.get(id=interpreter_id)
        _ = interpreter.create_messages()
        interpretation = interpreter.interpret_reading()
        return {"interpretation": interpretation, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}