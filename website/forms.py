from django import forms
from website.models import Product, Category, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Choose Products"
    )

    class Meta:
        model = Order
        fields = ['products']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
