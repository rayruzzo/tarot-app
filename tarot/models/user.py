from mongoengine import Document, StringField, IntField

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    age = IntField(min_value=13, max_value=120)
    meta = {'collection': 'users'}
    

class UserPassword(Document):
    user_id = StringField(required=True)
    password_hash = StringField(required=True)
    meta = {'collection': 'user_passwords'}

class JournalEntry(Document):
    userId = StringField(required=True)
    entry_date = StringField(required=True)
    readingId = StringField(required=True)
    content = StringField(required=True)
    meta = {'collection': 'journal_entries'}