from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
import os
import time
from django.core.paginator import Paginator
from django.apps import apps
from cart.models import CartItem
# Get the Dataset model using the app registry
dataset_model = apps.get_model('cart', 'Dataset')
# Create your views here.

def home(request):
    unchecked_cart_item_count = CartItem.objects.filter(cart__user=request.user, checked_out=False).count()
    print(unchecked_cart_item_count)
    return render(request,"base.html",{'unchecked_cart_item_count': unchecked_cart_item_count})

def dataset_list_sorted(request, sort_order='asc'):
    datasets = get_datasets_sorted_by_date(sort_order)
    paginator = Paginator(datasets, 5)  # Display 5 items per page
    page_number = request.GET.get('page')
    page_datasets = paginator.get_page(page_number)
    context = {'page_datasets': page_datasets, 'sort_order': sort_order}
    return render(request, 'genel/datasets.html', context)

def get_datasets_sorted_by_date(sort_order='asc'):
    dataset_dir = 'cart/static/cart/datasets/'
    datasets = dataset_model.objects.all()
    datasets_with_info = []
    for dataset in datasets:
        file_path = os.path.join(dataset.file.name)
        file_size = os.path.getsize(file_path)
        file_date = os.path.getctime(file_path)
        local_time = time.ctime(file_date)
        id=dataset.id
        datasets_with_info.append({'name': dataset.name, 'size': file_size, 'date': local_time, 'id':id})

    sorted_datasets = sorted(datasets_with_info, key=lambda x: x['date'], reverse=(sort_order == 'desc'))
    return sorted_datasets

"""
#@login_required
def dataset_list(request):
    datasets = Dataset.objects.all()
    paginator = Paginator(datasets, 5)  # Show 5 datasets per page
    page_number = request.GET.get('page')
    page_datasets = paginator.get_page(page_number)
    context = {'page_datasets': page_datasets}
    return render(request, 'genel/datasets.html', context)
    
"""
