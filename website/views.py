from django.shortcuts import render

from website.models import Product


def article_index(request):
    articles = Product.objects.all()
    return render(request, 'website/products/index.html', {'articles': articles})