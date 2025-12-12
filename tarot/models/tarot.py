from enum import Enum
from mongoengine import Document, StringField, EnumField, ListField, IntField, GenericReferenceField, ReferenceField

class TarotCard(Document):
    type = StringField(required=True)
    name_short = StringField(required=True)
    name = StringField(required=True)
    value = StringField(required=True)
    value_int = IntField(required=True)
    meaning_up = StringField(required=True)
    meaning_rev = StringField(required=True)
    desc = StringField(required=True)
    img = StringField(required=True)
    meta = {'collection': 'tarot_cards'}

    def __str__(self):
        return self.name + ": " + self.meaning_up + " / " + self.meaning_rev

    def to_dict(self):
        return {
            "type": self.type,
            "name_short": self.name_short,
            "name": self.name,
            "value": self.value,
            "value_int": self.value_int,
            "meaning_up": self.meaning_up,
            "meaning_rev": self.meaning_rev,
            "desc": self.desc,
            "img": self.img
        }

class ReadingType(Enum):
    PPF = "past_present_future"
    LILIA = "lilias_safe_passage"


class PPFReading(Document):
    cards = IntField(required=True, default=3)
    past = ReferenceField(TarotCard, required=True)
    present = ReferenceField(TarotCard, required=True)
    future = ReferenceField(TarotCard, required=True)
    meta = {'collection': 'ppf_readings'}

    def __str__(self):
        past = "Past: " + str(self.past.name)
        present = "Present: " + str(self.present.name)
        future = "Future: " + str(self.future.name)
        return past + " / " + present + " / " + future
    
    def to_dict(self):
        return {
            "past": self.past.to_dict(),
            "present": self.present.to_dict(),
            "future": self.future.to_dict()
        }
    
class LiliaReading(Document):
    cards = IntField(required=True, default=7)
    traveler = ReferenceField(TarotCard, required=True)
    what_is_missing = ReferenceField(TarotCard, required=True)
    path_behind = ReferenceField(TarotCard, required=True)
    path_ahead = ReferenceField(TarotCard, required=True)
    obstacles = ReferenceField(TarotCard, required=True)
    windfall = ReferenceField(TarotCard, required=True)
    destination = ReferenceField(TarotCard, required=True)
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

    def to_dict(self):
        return {
            "traveler": self.traveler.to_dict(),
            "what_is_missing": self.what_is_missing.to_dict(),
            "path_behind": self.path_behind.to_dict(),
            "path_ahead": self.path_ahead.to_dict(),
            "obstacles": self.obstacles.to_dict(),
            "windfall": self.windfall.to_dict(),
            "destination": self.destination.to_dict()
        }

class Reading(Document):
    user = StringField(required=True)
    question = StringField(required=True)
    readingType = EnumField(ReadingType, required=True)
    cards = GenericReferenceField(required=True)
    reversals = ListField(required=True)
    interpretation = StringField(required=False, default="")
    meta = {'collection': 'readings'}
    def __str__(self):
        cardString = self.cards.__str__()
        return self.user + " - " + self.question + " - " + cardString
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "user": self.user,
            "question": self.question,
            "readingType": self.readingType.name,
            "cards": self.cards.to_dict(),
            "reversals": self.reversals,
            "interpretation": self.interpretation
        }