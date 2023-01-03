from tkinter.ttk import Widget
from django import forms
from .choices import ShortRoleType

class SignUpForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    role = forms.ChoiceField(choices= ShortRoleType.choices)
