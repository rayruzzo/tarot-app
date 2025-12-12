import mongoengine
import requests
import random

from mongoengine.errors import ValidationError
from ..models import Reading, LiliaReading, PPFReading, ReadingType, TarotCard
from ..config.tarot import TAROT_API_URL

model_dispatcher = {
    ReadingType.LILIA: LiliaReading,
    ReadingType.PPF: PPFReading,
}

def checkTarotCard(card: dict) -> TarotCard:
    """Check database for existing tarot card, return if found, otherwise create and return new card"""
    cards = TarotCard.objects(name=card['name'])
    if len(cards) == 1:
        return cards[0]
    elif len(cards) > 1:
        raise ValidationError(f"Multiple tarot cards found with name {card['name']}")
    else:
        new_card = TarotCard(
            type=card['type'],
            name_short=card['name_short'],
            name=card['name'],
            value=card['value'],
            value_int=card['value_int'],
            meaning_up=card['meaning_up'],
            meaning_rev=card['meaning_rev'],
            desc=card['desc'],
            img=f"/media/tarot/cards/{card['name'].replace(' ', '_')}.jpg"
            ) 
        new_card.save()
        return new_card   

def getTarotCardsfromAPI(n: int) -> list:
    """Fetch tarot cards from API and save to database"""
    response = requests.get(TAROT_API_URL + "api/v1/cards/random?n={n}".format(n=n))
    data = response.json()["cards"]
    cardData = []
    for card in data:
        card = checkTarotCard(card)
        reversal = bool(random.getrandbits(1))
        cardData.append({"card": card, "reversal": reversal})
    return cardData


def createReading(userId, question, readingType) -> Reading | None:
    try:
        readingModel = model_dispatcher[readingType]
        num_cards = None
        
        if hasattr(readingModel, "_fields") and "cards" in readingModel._fields:
            num_cards = readingModel._fields["cards"].default
        else:
            raise ValueError(f"Reading type {readingType} does not support card drawing")

        # Draw the cards using the resolved number
        cards_drawn = getTarotCardsfromAPI(num_cards)
        cards = [card['card'] for card in cards_drawn]
        reversals = [card['reversal'] for card in cards_drawn]

        readingKwargs = {
            field: cards[i] for i, field in enumerate(readingModel._fields.keys()) if field not in ["cards", "meta" ]
        }
        # Create the reading instance
        readingInstance = readingModel(**readingKwargs).save()

        reading = Reading()
        reading.user = userId
        reading.question = question
        reading.reading_type = readingType
        reading.cards = readingInstance
        reading.reversals = reversals
        reading.save()

        return reading
    except Exception as e:
        print(f"Error creating reading: {e}")
        return None
    
def getReadingById(readingId: str) -> Reading | None:
    try:
        return Reading.objects.get(id=readingId)
    except (ValidationError, mongoengine.DoesNotExist):
        return None
    
def getReadingsByUser(userId: str) -> list:
    try:
        return Reading.objects(user=userId).all()
    except ValidationError:
        return []
    
def deleteReading(readingId: str) -> bool:
    try:
        reading = Reading.objects.get(id=readingId)
        reading.delete()
        return True
    except (ValidationError, mongoengine.DoesNotExist):
        return False