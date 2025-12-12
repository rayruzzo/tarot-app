from mongoengine import Document, StringField, IntField, DateTimeField
from django.contrib.auth.hashers import make_password, check_password
from enum import Enum

class ZodiacSign(Enum):
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"

def _get_zodiac_sign(dob):
    month = dob.month
    day = dob.day
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return ZodiacSign.ARIES.value
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return ZodiacSign.TAURUS.value
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return ZodiacSign.GEMINI.value
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return ZodiacSign.CANCER.value
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return ZodiacSign.LEO.value
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return ZodiacSign.VIRGO.value
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return ZodiacSign.LIBRA.value
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return ZodiacSign.SCORPIO.value
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return ZodiacSign.SAGITTARIUS.value
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return ZodiacSign.CAPRICORN.value
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return ZodiacSign.AQUARIUS.value
    else:
        return ZodiacSign.PISCES.value

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    dob = DateTimeField(required=True)
    age = IntField(required=True)
    meta = {'collection': 'users'}

    @property
    def sign(self):
        return _get_zodiac_sign(self.dob)

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