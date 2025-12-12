from django.forms import Form, DateField, DateInput, CharField, Textarea

class journalEntryForm(Form):
    date = DateField(widget=DateInput(attrs={'type': 'date'}))
    description = CharField(widget=Textarea(attrs={'rows': 4, 'cols': 50}))