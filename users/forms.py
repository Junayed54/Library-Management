from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SignUpForm(UserCreationForm):
	username = forms.CharField(label="User Name", max_length=100, widget=forms.TextInput(attrs={'class':'block text-gray-700 text-sm font-bold mb-2', 'placeholder':'User Name'}))
	email = forms.CharField(label="Email", max_length=100, widget=forms.EmailInput(attrs={'class':'block text-gray-700 text-sm font-bold mb-2', 'placeholder': 'Enter your email'}) )
	first_name = forms.CharField(label="First name", max_length=100, widget=forms.TextInput(attrs={'class':'block text-gray-700 text-sm font-bold mb-2', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="Last name", max_length=100, widget=forms.TextInput(attrs={'class':'block text-gray-700 text-sm font-bold mb-2', 'placeholder':'Last Name'}))
	password1 = forms.CharField(label = 'Password', max_length = 100, widget=forms.PasswordInput(attrs={'class':'block text-gray-700 text-sm font-bold mb-2', 'placeholder':"Enter your password"}))
	password2 = forms.CharField(label = 'Retype Password', max_length = 100, widget=forms.PasswordInput(attrs={'class':'block text-gray-700 text-sm font-bold mb-2', 'placeholder': 'Retype password'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
		
class SignInForm(forms.Form):
    	
    username = forms.CharField(label="User Name", max_length=100, widget=forms.TextInput(attrs={'class':'block text-gray-700 text-sm font-bold mb-2', 'placeholder':'User Name'}))
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={'class':'block text-gray-700 text-sm font-bold mb-2', 'placeholder':"Enter your password"}))    
    
    # class Meta:
    #     model = User
    #     fields = ['username', 'password']