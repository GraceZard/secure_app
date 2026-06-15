from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from inventory.models import Item
from .cart import Cart
from .forms import OrderForm
from .models import Order, OrderItem
from audit.models import AuditLog   # <-- for audit log

def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(item=item, quantity=quantity, override_quantity=False)
    return redirect('cart:detail')

def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart:detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    item=item['item'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Log the purchase
            AuditLog.objects.create(
                user=request.user,
                action='Purchase',
                details=f"Order #{order.id} placed: {order.items.count()} items, total RM {order.get_total_price()}",
                ip_address=get_client_ip(request)
            )
            cart.clear()
            return redirect('cart:order_created', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'cart/checkout.html', {'form': form, 'cart': cart})

def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cart/order_created.html', {'order': order})

def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        orders = []
    return render(request, 'cart/order_history.html', {'orders': orders})