from django.shortcuts import render, get_object_or_404, redirect
from website.forms import ProductForm
from website.models import Product


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
    global productForm
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