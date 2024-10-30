from website.models import Product, Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from .forms import ProductForm, SignupForm, LoginForm, OrderForm
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
    return redirect('product_index')

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

def order_list(request):
    orders = Order.objects.filter(user=request.user)

    for order in orders:
        total = sum(item.product.price * item.quantity for item in order.order_items.all())
        order.total = total

    return render(request, 'website/orders/list.html', {'orders': orders})


def add_product_to_order(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)

    order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)
    if not item_created:
        order_item.quantity += 1
        order_item.save()
    return redirect('product_index')

def order_item_delete(request, product_id):
    order_item = get_object_or_404(OrderItem, order__user=request.user, order__is_completed=False, product_id=product_id)
    order_item.delete()
    return redirect('order_list')

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