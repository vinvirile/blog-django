from django import forms

class LoginForm(forms.Form):
    # indetifier could be either username or password
    identifier = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput())
