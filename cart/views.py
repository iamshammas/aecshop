import uuid
from itertools import product

from django.shortcuts import render, redirect, get_object_or_404
from shop.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist


def get_cart_id(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart_id = str(uuid.uuid4())
        request.session['cart_id'] = cart_id
    return cart_id

def cart_details(request, tot=0, count=0, cart_items=None):
    c_id_val = get_cart_id(request)
    ct_items = []
    try:
        ct = cartlist.objects.get(cart_id=c_id_val)
        ct_items = items.objects.filter(cart=ct, active=True)
        for i in ct_items:
            tot += (i.prodt.price*i.qty)
            count += i.qty
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', {'ci': ct_items, 't': tot, 'cn': count})


def c_id(request):
    ct_id = request.session.session_key
    if not ct_id:
        request.session.cycle_key()
        ct_id = request.session.session_key
    return get_cart_id(request)


def add_cart(request,product_id):
    prod = products.objects.get(id=product_id)
    c_id_val = get_cart_id(request)  # use get_cart_id function to get the cart ID
    try:
        ct = cartlist.objects.get(cart_id=c_id_val)
    except cartlist.DoesNotExist:
        ct = cartlist.objects.create(cart_id=c_id_val)
        ct.save()
    try:
        c_items = items.objects.get(prodt=prod,cart=ct)
        if c_items.qty < c_items.prodt.stock:
            c_items.qty += 1  # increment the quantity correctly
        c_items.save()
    except items.DoesNotExist:
        c_items=items.objects.create(prodt=prod,qty=1,cart=ct)
        c_items.save()

    return redirect('cartDetails')



def min_cart(request,product_id):
    ct = cartlist.objects.get(cart_id=get_cart_id(request))
    prod = get_object_or_404(products,id=product_id)
    c_items = items.objects.get(prodt=prod,cart=ct)
    if c_items.qty > 1:
        c_items.qty -=1
        c_items.save()
    else:
        c_items.delete()
    return redirect('cartDetails')

def cart_delete(request,product_id):
    ct = cartlist.objects.get(cart_id=get_cart_id(request))
    prod = get_object_or_404(products,id=product_id)
    c_items = items.objects.get(prodt=prod,cart=ct)
    c_items.delete()
    return redirect('cartDetails')