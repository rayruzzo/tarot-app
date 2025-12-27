from django.forms import Form, EmailField, CharField, PasswordInput, ValidationError, DateField

class signUpForm(Form):
    username = CharField(max_length=100)
    email = EmailField()
    password = CharField(widget=PasswordInput())
    confirm_password = CharField(widget=PasswordInput())
    dob = DateField(label='Date of Birth')
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data