from django.forms import Form, Textarea, CharField, Textarea
from ..models import GuidedQuestions

class GuidedJournalEntryForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value in GuidedQuestions:
            self.fields[value.name.lower()] = CharField(
                widget=Textarea(attrs={'rows': 4, 'cols': 50}),
                label=value.value
            )

class FreeFormJournalEntryForm(Form):
    entry_text = CharField(widget=Textarea(attrs={'rows': 10, 'cols': 50}), label="Journal Entry Text")