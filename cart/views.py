from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from products.models import Product
from django.contrib import messages


CART_SESSION_KEY = 'cart'
WISHLIST_SESSION_KEY = 'wishlist'


def _get_cart(session):
    cart = session.get(CART_SESSION_KEY)
    if cart is None:
        cart = {}
        session[CART_SESSION_KEY] = cart
    return cart


def _get_wishlist(session):
    wishlist = session.get(WISHLIST_SESSION_KEY)
    if wishlist is None:
        wishlist = []
        session[WISHLIST_SESSION_KEY] = wishlist
    return wishlist


def cart_detail(request: HttpRequest):
    cart = _get_cart(request.session)
    items = []
    total = 0
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = int(item['quantity'])
        price = float(item['price'])
        subtotal = quantity * price
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal,
        })
    return render(request, 'cart/cart_detail.html', {'items': items, 'total': total})


def wishlist_toggle(request: HttpRequest, product_id: int):
    wishlist = _get_wishlist(request.session)
    pid = int(product_id)
    if pid in wishlist:
        wishlist.remove(pid)
    else:
        wishlist.append(pid)
    request.session[WISHLIST_SESSION_KEY] = wishlist
    request.session.modified = True
    return redirect('product_detail', slug=get_object_or_404(Product, id=pid).slug)


def wishlist_detail(request: HttpRequest):
    wishlist = _get_wishlist(request.session)
    products = Product.objects.filter(id__in=wishlist)
    return render(request, 'cart/wishlist.html', {'products': products})


def cart_add(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request.session)
    item = cart.get(str(product.id), {'quantity': 0, 'price': str(product.price)})
    new_qty = int(item['quantity']) + 1
    if new_qty > product.stock:
        messages.warning(request, f"Only {product.stock} in stock for {product.name}.")
        return redirect('cart_detail')
    item['quantity'] = new_qty
    cart[str(product.id)] = item
    request.session.modified = True
    messages.success(request, f"Added {product.name} to cart.")
    return redirect('cart_detail')


def cart_remove(request: HttpRequest, product_id: int):
    cart = _get_cart(request.session)
    cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect('cart_detail')


def cart_update(request: HttpRequest, product_id: int):
    quantity = int(request.POST.get('quantity', 1))
    cart = _get_cart(request.session)
    if str(product_id) in cart:
        product = get_object_or_404(Product, id=product_id)
        quantity = max(1, quantity)
        if quantity > product.stock:
            quantity = product.stock
            messages.warning(request, f"Quantity reduced to {product.stock} due to stock limits.")
        cart[str(product_id)]['quantity'] = quantity
        request.session.modified = True
        messages.success(request, "Cart updated.")
    return redirect('cart_detail')

# Create your views here.
