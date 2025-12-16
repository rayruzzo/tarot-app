from mongoengine import Document, StringField, ListField, DictField, FloatField, IntField
from .tarot import Reading

import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

class TarotInterpreter(Document):
    readingId = StringField(required=True)
    systemPrompt = StringField()
    messages = ListField(DictField(), required=False)
    interpretation = StringField(required=False)
    meta = {'collection': 'interpretations'}

    def create_messages(self):
        reading = Reading.objects(id=self.readingId).first()
        question = reading.question
        readingInstance = reading.cards
        reversals = reading.reversals
        fields = [key for key in readingInstance._fields if key not in ['id', '_id', 'cards', 'meta']]
        kwargs = {}
        for i in range(len(fields)):
            card = readingInstance[fields[i]]
            if reversals[i]:
                kwargs[fields[i]] = f"{card['name']} (reversed) - {card['meaning_rev']}"
            else:
                kwargs[fields[i]] = f"{card['name']} - {card['meaning_up']}"
        
        self.messages = [
            {"role": "system", "content": self.systemPrompt},
            {
                "role": "user", 
                "content": f"""Based on the following tarot reading, provide a detailed interpretation: \nQuestion: {question} Cards:{kwargs}"""
            },
        ]
        self.save()
        return self.messages
    
    def interpret_reading(self):
        messages = self.create_messages()
        request = LLMRequest(messages=messages)
        interpretation = request.make_request()
        # Ensure interpretation is a string
        if interpretation is None:
            interpretation = ""
        else:
            interpretation = str(interpretation)
        self.interpretation = interpretation
        self.save()

        reading = Reading.objects(id=self.readingId).first()
        if reading:
            reading.interpretator = self
            reading.save()
        
        return interpretation
    

    def get_reading(self):
        return Reading.objects(id=self.readingId).first()
    
    
class LLMRequest(Document):
    model = StringField(required=True, default="gpt-4o-mini")
    messages = ListField(DictField(), required=True)
    temperature = FloatField(default=0.7)
    max_tokens = IntField(default=500)

    def to_dict(self):
        return {
            "model": self.model,
            "input": self.messages,
            "temperature": self.temperature,
            "max_output_tokens": self.max_tokens
        }
    
    def make_request(self):
        client = openai.Client()
        response = client.responses.create(**self.to_dict())

        return response.output_text