from enum import Enum
from datetime import datetime
from mongoengine import Document, StringField, IntField, DateTimeField

class JournalEntryType(Enum):
    GUIDED = 1
    FREEFORM = 0

class GuidedQuestions(Enum):
    FEEL = "What was your initial reaction or intuitive response when you first saw the cards?"
    NOTICE = "Which card(s) stood out most strongly to you? What associations did it bring up?"
    CONNECT = "What patterns did you notice between the cards? How do these patterns relate to your current situation?"
    CONTEXT = "How does this reading connect to your current life situation or the question you brought to it?"
    ACTION = "What shift in perspective or action does this reading invite you to consider? "


class BaseJournalEntry(Document):
    readingId = StringField(required=True, unique=True)
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)
    type = IntField(required=True, choices=[e.value for e in JournalEntryType])
    meta = {'allow_inheritance': True,
            'collection': 'journal_entries'}

class GuidedJournalEntry(BaseJournalEntry):
    feel = StringField()
    notice = StringField()
    connect = StringField()
    context = StringField()
    action = StringField()

    def to_dict(self):
        return {
            'id': str(self.id),
            '_id': str(self.id),
            'readingId': self.readingId,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'type': self.type,
            'feel': self.feel,
            'notice': self.notice,
            'connect': self.connect,
            'context': self.context,
            'action': self.action
        }

class FreeFormJournalEntry(BaseJournalEntry):
    content = StringField()

    def to_dict(self):
        return {
            'id': str(self.id),
            '_id': str(self.id),
            'readingId': self.readingId,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'type': self.type,
            'content': self.content
        }