
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import PurchasedItem
from cart.models import Cart,CartItem
# Create your views here.
def register(request):
    if request.method== 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('genel:home')
    else:
        form=UserRegisterForm()

    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    u_form=UserUpdateForm()
    p_form=ProfileUpdateForm()
    purchased_items = PurchasedItem.objects.filter(user=request.user)
    print(purchased_items)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'purchased_items': purchased_items,  # Fetch the purchased items as a queryset
    }
    return render(request,"users/profile.html",context)


