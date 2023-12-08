# in your app directory, create a new file named forms.py
from django import forms

from authentification.models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
class Register(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','role'] 
        # Add custom widgets or validations if needed
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }