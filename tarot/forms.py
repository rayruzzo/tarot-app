from django import forms

READING_CHOICES = [
    ('past_present_future', 'Past / Present / Future'),
    ('safe_passage', "Lilia's Safe Passage"),
]

class readingForm(forms.Form):
    name = forms.CharField(
        label="First, what is your name?", 
        max_length=200, 
        widget=forms.TextInput(attrs={'class':'form-control my-3'})
    )
    question = forms.CharField(
        label="What is on your mind?",
        widget=forms.Textarea(attrs={'class':'form-control my-3'})
    )
    reading_type = forms.ChoiceField(
        label="Choose a reading type",
        choices=READING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select my-3'})
    )

    class Meta:
        initial = {'name': 'Our Friend'}
