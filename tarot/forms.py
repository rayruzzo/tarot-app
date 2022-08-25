from django import forms

class readingForm(forms.Form):
    name = forms.CharField(label="First, what is your name?", max_length=200, widget=forms.TextInput(attrs={'class':'form-control my-3'}))
    question = forms.CharField(label="What is on your mind?",widget=forms.Textarea(attrs={'class':'form-control my-3'}))

    class Meta:
        initial = {'name': 'Our Friend'}