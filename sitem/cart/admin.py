from django.contrib import admin
from .models import Cart,CartItem,Dataset
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Dataset)