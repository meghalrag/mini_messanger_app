from django import forms
class LoginForm(forms.Form):
    email=forms.CharField(max_length=50,required=True,
    widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'email'}))
    password=forms.CharField(max_length=50,required=True,
    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))
class RegForm(forms.Form):
    email=forms.CharField(max_length=50,required=True,
    widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'enter email'}))
    passwordreg=forms.CharField(min_length=8,required=True,
    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'enter password'}))
    cpasswordreg=forms.CharField(min_length=8,required=True,
    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'enter password again'}))