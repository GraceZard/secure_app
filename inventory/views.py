from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.http import require_POST
from audit.models import AuditLog
from .models import Item
from .forms import ItemForm


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('inventory:item_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('inventory:item_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('inventory:item_list')
    template_name = 'inventory/item_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def log_stock_action(request, action, item, old_quantity, new_quantity):
    AuditLog.objects.create(
        user=request.user,
        action=action,
        details=(
            f"Item: {item.name} (ID: {item.pk}); "
            f"quantity changed from {old_quantity} to {new_quantity}"
        ),
        ip_address=get_client_ip(request),
    )


@login_required
@require_POST
def stock_in(request, pk):
    if request.user.role != 'admin':
        raise PermissionDenied

    with transaction.atomic():
        item = get_object_or_404(Item.objects.select_for_update(), pk=pk)
        old_quantity = item.quantity
        item.quantity += 1
        item.save(update_fields=['quantity'])
        log_stock_action(request, 'Stock In', item, old_quantity, item.quantity)

    messages.success(request, f"Stock IN: Added 1 to '{item.name}'. New quantity: {item.quantity}")
    return redirect('inventory:item_list')


@login_required
@require_POST
def stock_out(request, pk):
    if request.user.role != 'admin':
        raise PermissionDenied

    with transaction.atomic():
        item = get_object_or_404(Item.objects.select_for_update(), pk=pk)
        if item.quantity <= 0:
            messages.error(request, f"Cannot remove stock: '{item.name}' quantity is already zero.")
            return redirect('inventory:item_list')

        old_quantity = item.quantity
        item.quantity -= 1
        item.save(update_fields=['quantity'])
        log_stock_action(request, 'Stock Out', item, old_quantity, item.quantity)

    messages.success(request, f"Stock OUT: Removed 1 from '{item.name}'. New quantity: {item.quantity}")
    return redirect('inventory:item_list')
