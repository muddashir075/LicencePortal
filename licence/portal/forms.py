from typing import Any
from django import forms
from .models import User
from .models import Licence_Data
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserRegistrationForm (forms.ModelForm):
    role = forms.ChoiceField(choices = [('resourse', 'Resourse'), ('manager', 'Manager'), ('admin', 'Admin')], initial='resourse')
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model= User
        fields = ['username', 'password', 'password_confirm', 'role']

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role == 'admin':
            if User.objects.filter(role='admin').exists():
                raise forms.ValidationError("Only one Admin is Allow and it is already exists")
        return role

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        return cleaned_data
    
    def save(self, commit= True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
        
        '''if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwod do not match!")
        if self.instance.pk and self.instance.role != cleaned_data['role']:
            if cleaned_data['role'] in ['admin', 'manager']:
                if cleaned_data['role'] == 'admin' and User.objects.filter(role='admin').exists():
                    raise forms.ValidationError("Only one admin user is allowed")
                pass
            else:
                pass
        return cleaned_data
'''
class LicenceForm(forms.ModelForm):
    class Meta:
        model = Licence_Data
        fields = ['name','image','pdf']