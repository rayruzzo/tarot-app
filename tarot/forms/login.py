from django.forms import Form, CharField, ValidationError, PasswordInput

class loginForm(Form):
    email = CharField(max_length=100)
    password = CharField(widget=PasswordInput())
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if not email or not password:
            raise ValidationError("Both email and password are required.")
        return cleaned_data