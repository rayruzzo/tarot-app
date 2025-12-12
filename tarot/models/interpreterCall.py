from mongoengine import Document, StringField, ListField, DictField, FloatField, IntField
from .tarot import Reading

import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

class AIPrompt(Document):
    readingId = StringField(required=True)
    systemPrompt = StringField()
    meta = {'collection': 'AI_prompts'}

    def create_messages(self):
        reading = Reading.objects(id=self.readingId).first()
        readingInstance = reading.cards
        reversals = reading.reversals
        fields = [key for key in readingInstance.keys() if key not in ['id', '_id', 'cards', 'meta']]
        kwargs = {}
        for i in range(len(fields)):
            card = readingInstance[fields[i]]
            if reversals[i]:
                kwargs[fields[i]] = f"{card['name']} (reversed) - {card['meaning_rev']}"
            else:
                kwargs[fields[i]] = f"{card['name']} - {card['meaning-up']}"
        
        self.messages = [
            {"role": "system", "content": self.systemPrompt},
            {"role": "user", "content": f"Based on the following tarot reading, provide a detailed interpretation: {kwargs}"},
            ]
        return self.messages
    
class LLMRequest(Document):
    model = StringField(required=True, default="gpt-4o-mini")
    messages = ListField(DictField(), required=True)
    temperature = FloatField(default=0.7)
    max_tokens = IntField(default=500)

    def to_dict(self):
        return {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    def make_request(self):
        response = openai.ChatCompletion.create(**self.to_dict())
        return response['choices'][0]['message']['content']