import stripe
from django.conf import settings
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

#Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user, is_completed=False)
    line_items = []

    for item in order.order_items.all():
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': item.product.title,
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/payment/success/') + f"?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=request.build_absolute_uri('/payment/cancel/'),
        metadata={
            'order_id': order.id
        }
    )

    return redirect(session.url)


def payment_success(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == 'paid':
        order = Order.objects.get(id=session.metadata.order_id, user=request.user)
        order.is_completed = True
        order.save()

    return render(request, 'website/stripe/payment_success.html')



def payment_cancel(request):
    return render(request, 'website/stripe/payment_cancel.html')

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