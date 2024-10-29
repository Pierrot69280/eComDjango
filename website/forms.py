from django import forms
from website.models import Product, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
