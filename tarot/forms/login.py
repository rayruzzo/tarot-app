from django.forms import Form, CharField, ValidationError, PasswordInput

class loginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username or not password:
            raise ValidationError("Both username and password are required.")
        return cleaned_data