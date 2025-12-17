from enum import Enum
from datetime import datetime
from mongoengine import Document, StringField, EnumField, ListField, IntField, GenericReferenceField, ReferenceField, DateTimeField

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
        # Only return direct fields, no references
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
    SINGLE = "single_card"

class Reading(Document):
    created_at = DateTimeField(required=True, default=datetime.utcnow)
    user = StringField(required=True)
    question = StringField(required=True)
    readingType = EnumField(ReadingType, required=True)
    cards = GenericReferenceField(required=True)
    reversals = ListField(required=True)
    interpretator = GenericReferenceField(required=False)
    journal = GenericReferenceField(required=False)
    meta = {'collection': 'readings'}
    def __str__(self):
        cardString = self.cards.__str__()
        return self.user + " - " + self.question + " - " + cardString
    
    def to_dict(self):
        interpretation = self.interpretator.interpretation if hasattr(self.interpretator, 'interpretation') else None
        created_at_str = self.created_at.strftime("%m/%d/%y") if self.created_at else None
        journal_dict = self.journal.to_dict() if self.journal else None
        return {
            "_id": str(self.id),
            "id": str(self.id),
            "created_at": created_at_str,
            "user": self.user,
            "question": self.question,
            "readingType": self.readingType.name,
            "cards": self.cards.to_dict(),
            "reversals": self.reversals,
            "interpretation": interpretation,
            "journal": journal_dict
        }
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
        # Only serialize referenced TarotCard fields, not the whole reading
        return {
            "past": self.past.to_dict() if self.past else None,
            "present": self.present.to_dict() if self.present else None,
            "future": self.future.to_dict() if self.future else None
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
        # Only serialize referenced TarotCard fields, not the whole reading
        return {
            "traveler": self.traveler.to_dict() if self.traveler else None,
            "what_is_missing": self.what_is_missing.to_dict() if self.what_is_missing else None,
            "path_behind": self.path_behind.to_dict() if self.path_behind else None,
            "path_ahead": self.path_ahead.to_dict() if self.path_ahead else None,
            "obstacles": self.obstacles.to_dict() if self.obstacles else None,
            "windfall": self.windfall.to_dict() if self.windfall else None,
            "destination": self.destination.to_dict() if self.destination else None
        }
        
class SingleCardReading(Document):
    cards = IntField(required=True, default=1)
    card = ReferenceField(TarotCard, required=True)
    meta = {'collection': 'single_card_readings'}

    def __str__(self):
        return "Card: " + str(self.card.name)
    
    def to_dict(self):
        return {
            "card": self.card.to_dict() if self.card else None
        }