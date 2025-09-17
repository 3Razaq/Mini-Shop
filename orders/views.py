from django.shortcuts import render, redirect
from django import forms
from .models import Order, OrderItem, Address, Payment
from django.contrib import messages


class CheckoutForm(forms.Form):
    # Shipping
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30)
    line1 = forms.CharField(label='Address line 1', max_length=200)
    line2 = forms.CharField(label='Address line 2', max_length=200, required=False)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100, required=False)
    postal_code = forms.CharField(max_length=20)
    country = forms.CharField(max_length=50, initial='US')
    use_shipping_as_billing = forms.BooleanField(required=False, initial=True, label='Billing same as shipping')
    # Billing (optional; used if checkbox unchecked)
    bill_full_name = forms.CharField(max_length=150, required=False)
    bill_email = forms.EmailField(required=False)
    bill_phone = forms.CharField(max_length=30, required=False)
    bill_line1 = forms.CharField(max_length=200, required=False)
    bill_line2 = forms.CharField(max_length=200, required=False)
    bill_city = forms.CharField(max_length=100, required=False)
    bill_state = forms.CharField(max_length=100, required=False)
    bill_postal_code = forms.CharField(max_length=20, required=False)
    bill_country = forms.CharField(max_length=50, required=False)


def checkout(request):
    from products.models import Product
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # stock validation
            from products.models import Product
            for product_id, item in cart.items():
                product = Product.objects.get(id=product_id)
                quantity = int(item['quantity'])
                if quantity > product.stock:
                    messages.error(request, f"Insufficient stock for {product.name} (only {product.stock}).")
                    return redirect('cart_detail')

            # create shipping address
            ship = Address.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                line1=form.cleaned_data['line1'],
                line2=form.cleaned_data.get('line2', ''),
                city=form.cleaned_data['city'],
                state=form.cleaned_data.get('state', ''),
                postal_code=form.cleaned_data['postal_code'],
                country=form.cleaned_data.get('country', 'US'),
            )
            if form.cleaned_data.get('use_shipping_as_billing'):
                bill = ship
            else:
                bill = Address.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    full_name=form.cleaned_data.get('bill_full_name') or form.cleaned_data['full_name'],
                    email=form.cleaned_data.get('bill_email') or form.cleaned_data['email'],
                    phone=form.cleaned_data.get('bill_phone') or form.cleaned_data['phone'],
                    line1=form.cleaned_data.get('bill_line1') or form.cleaned_data['line1'],
                    line2=form.cleaned_data.get('bill_line2') or '',
                    city=form.cleaned_data.get('bill_city') or form.cleaned_data['city'],
                    state=form.cleaned_data.get('bill_state') or form.cleaned_data.get('state', ''),
                    postal_code=form.cleaned_data.get('bill_postal_code') or form.cleaned_data['postal_code'],
                    country=form.cleaned_data.get('bill_country') or form.cleaned_data.get('country', 'US'),
                )

            order = Order(
                user=request.user if request.user.is_authenticated else None,
                shipping_address=ship,
                billing_address=bill,
                status='pending',
            )
            order.save()
            for product_id, item in cart.items():
                product = Product.objects.get(id=product_id)
                quantity = int(item['quantity'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                )
                product.stock = max(0, product.stock - quantity)
                product.save(update_fields=['stock'])
            # scaffold payment record
            Payment.objects.create(order=order, amount=order.total_amount, status='pending')
            request.session['cart'] = {}
            request.session.modified = True
            messages.success(request, f"Order placed successfully.")
            return redirect('order_confirm', order_id=order.id)
    else:
        form = CheckoutForm()

    items = []
    total = 0
    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = int(item['quantity'])
        subtotal = float(product.price) * quantity
        total += subtotal
        items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'orders/checkout.html', {'form': form, 'items': items, 'total': total})


def order_confirm(request, order_id: int):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/confirm.html', {'order': order})

# Create your views here.
