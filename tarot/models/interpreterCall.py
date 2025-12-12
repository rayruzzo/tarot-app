#model for making a call to OpenAI's API
from mongoengine import Document, StringField, ListField, DictField, FloatField, IntField
from .tarot import Reading

class AIPrompt(Document):
    userId = StringField(required=True)
    readingId = StringField(required=True)
    systemPrompt = StringField()

    def create_messages(self):
        reading = Reading.objects(id=self.readingId).first()
        cards = reading.cards if reading else []
        
        messages = [{"role": "system", "content": self.systemPrompt}]
        return messages

class LLMRequest(Document):
    model = StringField(required=True)
    messages = ListField(DictField(), required=True)
    temperature = FloatField()
    max_tokens = IntField()