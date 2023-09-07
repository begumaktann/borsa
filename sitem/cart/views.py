from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta,datetime
import secrets
from django.utils.datetime_safe import datetime
from django.utils import timezone
from django.http import HttpResponse, FileResponse
from django.contrib.sessions.models import Session
from .forms import UserInfoForm
from django.shortcuts import render, redirect, get_object_or_404
# from carton.cart import Cart
from .models import CartItem, Dataset, Cart, DownloadLink
from users.models import PurchasedItem

import os


def product_list(request):
    from .models import Dataset
    create_products_from_excel_files()
    datasets = Dataset.objects.all()
    context = {'datasets': datasets}
    return render(request, 'cart/product_list.html', context)


def create_products_from_excel_files():
    from .models import Dataset
    dataset_dir = 'cart/static/cart/datasets/'
    for file in os.listdir(dataset_dir):
        if file.endswith('.xls') or file.endswith('.xlsx'):
            product, created = Dataset.objects.get_or_create(
                name=file,  # Use the file name as the 'name' field value
                file=os.path.join(dataset_dir, file),  # Use the 'file' field
                price=10.00  # Set the appropriate price here
            )


def add_to_cart(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Create a CartItem and associate it with the Dataset
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        dataset=dataset,
        defaults={'quantity': 1}  # Default quantity is 1
    )
    cart_item.download_token = generate_download_token()
    cart_item.link_expiration = timezone.now() + timedelta(hours=24)  # Expiry in 24 hours
    cart_item.save()

    # Convert link_expiration to a string representation
    link_expiration_str = cart_item.link_expiration.strftime('%Y-%m-%dT%H:%M:%S')
    cart_item.link_expiration = link_expiration_str
    cart_item.save()
    # Append the download link data to the session
    download_links_data = request.session.get('download_links_data', [])
    download_links_data.append({
        'download_token': cart_item.download_token,
        'link_expiration': link_expiration_str,
    })
    request.session['download_links_data'] = download_links_data
    request.session.save()
    # Increment the quantity if the CartItem already existed
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('genel:datasets')



def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Check if the delete button was clicked
        delete_item_id = request.POST.get('delete_item_id')
        if delete_item_id:
            cart_item = get_object_or_404(CartItem, id=delete_item_id)
            cart_item.delete()
            return HttpResponseRedirect(request.path)
    # Get all cart items associated with this cart
    cart_items = CartItem.objects.filter(cart=cart, checked_out=False)

    total_price = sum(item.dataset.price * item.quantity for item in cart_items)
    has_items = len(cart_items) > 0

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'has_items': has_items,
    }

    return render(request, 'cart/view_cart.html', context)


def generate_download_token():
    return secrets.token_urlsafe(32)  # Generate a secure token


def download(request, token):
    cart_item = get_object_or_404(CartItem, download_token=token)
    current_time = timezone.localtime(timezone.now())
    if cart_item.link_expiration < current_time:
        return HttpResponse("Link has expired.")
    file_path = cart_item.dataset.file.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{cart_item.dataset.name}"'
    return response


def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    download_links_data = []
    if request.method == 'POST':
        user_info_form = UserInfoForm(request.POST)
        if user_info_form:
            # Save the user information to the user's profile or another appropriate model
            # You should replace 'profile' with your actual user profile model
            user_profile = request.user.profile  # Replace 'profile' with your actual user profile model
            user_profile.first_name = user_info_form.cleaned_data['first_name']
            user_profile.last_name = user_info_form.cleaned_data['last_name']
            user_profile.address = user_info_form.cleaned_data['address']
            user_profile.phone_number = user_info_form.cleaned_data['phone_number']
            user_profile.save()
            # Process the order and generate download links here
            # You can use cart items or other relevant data
            # Redirect to a confirmation page or payment gateway
            return redirect('cart:checkout')  # Replace 'order-confirmation' with the actual URL name
    else:
        user_profile = request.user.profile if hasattr(request.user, 'profile') else None # Replace 'profile' with your actual user profile model
        initial_data = {
            'first_name': user_profile.first_name if user_profile else '',
            'last_name': user_profile.last_name if user_profile else '',
            'address': user_profile.address if user_profile else '',
            'phone_number': user_profile.phone_number if user_profile else '',
        }
        user_info_form = UserInfoForm(initial=initial_data)
    cart_items = cart.cartitem_set.all()  # Get all cart items associated with this cart
    for cart_item in cart_items:
        cart_item.checked_out = True
        cart_item.save()
        download_links_data.append({
            'download_token': cart_item.download_token,
            'link_expiration': cart_item.link_expiration,
        })
    print(download_links_data)
    context = {'download_links_data': download_links_data,
               'user_info_form': user_info_form}
    return render(request, 'cart/checkout.html', context)




def download_link_check(request, url_token):
    download_links_data = request.session.get('download_links_data', [])  # Retrieve the stored data,
    print(download_links_data)
    for link_data in download_links_data:
        print("burda")
        if link_data['download_token'] == url_token:
            print("step1")
            link_expiration = link_data['link_expiration']
            link_expiration = timezone.datetime.strptime(link_expiration,'%Y-%m-%dT%H:%M:%S')
            link_expiration = timezone.make_aware(link_expiration, timezone.utc)  # Make it an aware datetime
            current_time = timezone.now()
            cart_item = get_object_or_404(CartItem, download_token=url_token)
            download_token = cart_item.download_token
            download_link, created = DownloadLink.objects.get_or_create(
                download_token=download_token,
                defaults={'link_expiration': cart_item.link_expiration}
            )
            purchased_item = PurchasedItem.objects.get_or_create(
                user=request.user,
                dataset=cart_item.dataset,
                download_link=download_link
            )

            if link_expiration >= current_time:
                cart_item = get_object_or_404(CartItem, download_token=url_token)
                cart=cart_item.cart
                file_path = cart_item.dataset.file.path
                response = FileResponse(open(file_path, 'rb'))
                response['Content-Disposition'] = f'attachment; filename="{cart_item.dataset.name}"'
                  # Clear the cart items
                #cart_item.delete()
                request.session.modified = True
                return response
            # Remove the link data from the list

            download_links_data.remove(link_data)
            request.session['download_links_data'] = download_links_data
            request.session.modified = True
            break
    else:
        return HttpResponse("Invalid or expired download link.")
    return HttpResponse("Download link checked successfully.")