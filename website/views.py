from website.models import Product
from django.contrib.auth import authenticate, login, logout
from .forms import ProductForm, SignupForm, LoginForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import CategoryForm
def product_index(request):
    products = Product.objects.all()
    return render(request, 'website/products/index.html', {'products': products})

def product_show(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'website/products/show.html', {'product': product})


def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_index_index')

def product_create(request):
    if request.method == "POST":
        productForm = ProductForm(request.POST)
        if productForm.is_valid():
            productForm.save()
            return redirect('product_index')
    else:
        productForm = ProductForm()
    return render(request, "website/products/create.html", {"productForm": productForm})
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        productForm = ProductForm(request.POST, instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('product_index')
    else:
        productForm = ProductForm(instance=product)
    return render(request, "website/products/edit.html", {"productForm": productForm})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'website/categories/index.html', {'categories': categories})

def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'website/categories/create.html', {'form': form})

def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'website/categories/edit.html', {'form': form, 'category': category})

def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'website/registration/signup.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('product_index')
    else:
        form = LoginForm()
    return render(request, 'website/registration/login.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect('login')