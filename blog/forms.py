from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("That username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def clean_password_confirmation(self):
        password = self.cleaned_data["password"]
        password_confirmation = self.cleaned_data["password_confirmation"]

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirmation
