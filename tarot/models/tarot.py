from enum import Enum
from mongoengine import Document, StringField, EnumField, ListField, IntField, GenericReferenceField

class TarotCard(Document):
    type = StringField(required=True)
    name_short = StringField(required=True)
    name = StringField(required=True)
    value = StringField(required=True)
    value_int = StringField(required=True)
    meaning_up = StringField(required=True)
    meaning_rev = StringField(required=True)
    desc = StringField(required=True)
    img = StringField(required=True)
    meta = {'collection': 'tarot_cards'}

    def __str__(self):
        return self.name + ": " + self.meaning_up + " / " + self.meaning_rev

class ReadingType(Enum):
    PPF = "past_present_future"
    LILIA = "lilias_safe_passage"


class PPFReading(Document):
    cards = IntField(required=True, default=3)
    past = TarotCard(required=True)
    present = TarotCard(required=True)
    future = TarotCard(required=True)
    meta = {'collection': 'ppf_readings'}

    def __str__(self):
        past = "Past: " + str(self.past.name)
        present = "Present: " + str(self.present.name)
        future = "Future: " + str(self.future.name)
        return past + " / " + present + " / " + future
    
class LiliaReading(Document):
    cards = IntField(required=True, default=7)
    traveler = TarotCard(required=True)
    what_is_missing = TarotCard(required=True)
    path_behind = TarotCard(required=True)
    path_ahead = TarotCard(required=True)
    obstacles = TarotCard(required=True)
    windfall = TarotCard(required=True)
    destination = TarotCard(required=True)
    meta = {'collection': 'lilia_readings'}
    def __str__(self):
        traveler = "Traveler: " + str(self.traveler.name)
        what_is_missing = "What is missing: " + str(self.what_is_missing.name)
        path_behind = "Path behind: " + str(self.path_behind.name)
        path_ahead = "Path ahead: " + str(self.path_ahead.name)
        obstacles = "Obstacles: " + str(self.obstacles.name)
        windfall = "Windfall: " + str(self.windfall.name)
        destination = "Destination: " + str(self.destination.name)
        return traveler + " / " + what_is_missing + " / " + path_behind + " / " + path_ahead + " / " + obstacles + " / " + windfall + " / " + destination


class Reading(Document):
    user = StringField(required=True)
    question = StringField(required=True)
    readingType = EnumField(ReadingType, required=True)
    cards = GenericReferenceField(required=True)
    reversals = ListField(required=True)
    meta = {'collection': 'readings'}
    def __str__(self):
        cardString = self.cards.__str__()
        return self.user + " - " + self.question + " - " + cardString