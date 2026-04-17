from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Order, OrderStatus
from .forms import OrderForm

def get_user_role(user):
    if not user.is_authenticated:
        return 'guest'
    if user.is_superuser:
        return 'admin'
    if user.groups.filter(name='Managers').exists():
        return 'manager'
    return 'client'

# Create your views here.
def order_list(request):
    user_role = get_user_role(request.user) if request.user.is_authenticated else 'guest'
    
    orders = Order.objects.select_related('status').all()

    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    if user_role == 'admin' or user_role == 'manager':
        if search_query:
            orders = orders.filter(
                Q(status__status__icontains=search_query) | 
                Q(id__icontains=search_query) 
            )

        
        if status_filter:
            orders = orders.filter(status_id=status_filter)

    
    paginator = Paginator(orders.order_by('-id'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    context = {
        'page_obj': page_obj,
        'user_role': user_role,
        'statuses': OrderStatus.objects.all(), 
        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(request, 'orders/order_list.html', context)


@login_required
def order_create(request):
    role = get_user_role(request.user)
    
    if role not in ['admin', 'manager']:
        messages.error(request, 'У вас нет прав на создание заказов.')
        return redirect('orders:order_list')

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ успешно создан')
            return redirect('orders:order_list')
    else:
        form = OrderForm()

    return render(request, 'orders/order_form.html', {
        'form': form,
        'title': 'Добавить заказ',
        'user_role': role 
    })



@login_required
def order_update(request,pk):
    role = get_user_role(request.user)
    
    if role not in ['admin', 'manager']:
        messages.error(request, 'У вас нет прав на создание заказов.')
        return redirect('orders:order_list')
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('orders:order_list')

    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'заказ обновлен.')
            return redirect('orders:order_list')
    else:
        form = OrderForm(instance=order)

    return render(request, 'orders/order_form.html', {
        'form': form,
        'order': order,
        'title': 'Редактировать заказ',
        'user_role': role
    })

@login_required
def order_delete(request,pk):
    role = get_user_role(request.user)
    
    if role not in ['admin', 'manager']:
        messages.error(request, 'У вас нет прав на создание заказов.')
        return redirect('orders:order_list')
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('orders:order_list')

    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order.delete()
        messages.success(request, 'заказ удален.')
        return redirect('orders:order_list')

    return render(request, 'orders/order_confirm_delete.html', {
        'order': order,
        'user_role': role
    })