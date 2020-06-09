from django import forms
from .models import Company,Common_User
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class Company_forms(forms.ModelForm):
    class Meta:
        model=Company
        fields="__all__"


# class User_form(UserCreationForm):
#     password=forms.CharField(label='password',widget=forms.PasswordInput)
#     class Meta:
#         model=User
#         fields=['username','email','password','password2']
#
# class Common_user_form(forms.ModelForm):
#     user=User_form(requried=True)
#     class Meta:
#         model=Common_User
#         fields=['user','invested']
#     def save(self, commit=True):