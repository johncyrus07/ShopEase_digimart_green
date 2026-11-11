from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import BaseUser
class RegisterForm(UserCreationForm):
 email=forms.EmailField(required=True)
 class Meta:
  model=BaseUser
  fields=['username','email','first_name','middle_name','last_name','gender','password1','password2']
