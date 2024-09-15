from operator import contains

from django.shortcuts import render, get_object_or_404
from sympy.integrals.meijerint_doc import category
from sympy.polys.polyconfig import query
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.db.models import Q
from .models import *


# Create your views here.
def home(request, c_slug=None):
    # Get the category if a slug is provided, otherwise set to None
    category = get_object_or_404(categ, slug=c_slug) if c_slug else None

    # Fetch products based on category filter, if category exists
    products_qs = products.objects.filter(category=category, available=True) if category else products.objects.filter(available=True)

    # Paginate the products queryset
    paginator = Paginator(products_qs, 3)  # Show 3 products per page
    page_number = request.GET.get('page', 1)

    try:
        products_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If the page number is not an integer, deliver the first page
        products_page = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        products_page = paginator.page(paginator.num_pages)

    # Get all categories to show in the context
    categories = categ.objects.all()

    context = {
        'products': products_page,  # Renamed for clarity
        'categories': categories,  # Renamed for clarity
        'selected_category': category,  # Optional: to track which category is selected
    }

    return render(request, 'index.html', context)



def prodDetails(request, c_slug, product_slug):
    try:
        prod = products.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'item.html', {'pr': prod})

def searching(request):
    prod = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        prod = products.objects.all().filter(Q(name__contains=query)|Q(desc__contains=query))
    return render(request,'search.html',{'qr':query,'pr':prod})