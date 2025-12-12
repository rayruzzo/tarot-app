from django.forms import Form, CharField, ChoiceField, Textarea, Select
from ..models.tarot import ReadingType 

def get_reading_choices():
    return [(rt.name, rt.value.replace('_', ' ').title()) for rt in ReadingType]


class readingForm(Form):
    question = CharField(
        label="What is on your mind?",
        widget=Textarea(attrs={'class':'form-control my-3'})
    )
    readingType = ChoiceField(
        label="Choose a reading type",
        choices=get_reading_choices(),
        widget=Select(attrs={'class': 'form-select my-3'})
    )
