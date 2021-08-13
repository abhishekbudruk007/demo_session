from django.contrib import admin
from .models import Product , Wishlist ,OrderItem , Order , CheckoutAddress
# Register your models here.
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CheckoutAddress)


