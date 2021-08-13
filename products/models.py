from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save ,post_delete
from users.models import UserLogs
from django_countries.fields import CountryField

QUANTITY_TYPE = (
    ('250GM','250 Grams'),
    ('500GM','500 Grams'),
    ('750GM','750 Grams'),
    ('1000GM','1 Kg'),
    ('1PC','1 Pc'),
    ('12PC','12 Pc')
)

PRODUCT_TYPE = (
    ('V','Vegetable'),
    ('F','Fruit')
)
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField(default=0.0)
    product_discount_price = models.FloatField(blank=True, null=True)
    product_quantity_type = models.CharField(choices=QUANTITY_TYPE, max_length=6)
    product_type = models.CharField(choices=PRODUCT_TYPE, max_length=1)
    description = models.TextField(max_length=500,blank=True,null=True)
    product_quantity =  models.IntegerField(blank=False,null=False)
    product_photo = models.ImageField(upload_to='products/', blank=False, null=False)
    def __str__(self):
        return self.product_name


class OrderItem(models.Model) :
    orderitem_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    orderitem_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    orderitem_ordered = models.BooleanField(default=False)
    orderitem_quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.orderitem_quantity} of {self.orderitem_product.product_name}"

    def get_total_item_price(self):
        return self.orderitem_quantity * self.orderitem_product.product_price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_address = models.ForeignKey(
        'CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment =models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_total_item_price()
        return total


class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Wishlist(models.Model):
    wishlist_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    wishlist_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    wishlist_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wishlist_product.product_name


@receiver(post_save, sender=Wishlist)
def post_save_wishlist(sender,**kwargs):
    print("Sender",sender)
    instance = kwargs["instance"]  # <Wishlist: Potatoes>
    userlogs_object, created = UserLogs.objects.get_or_create(
        userlogs_user=instance.wishlist_user,
        userlogs_action='wishlist_item_added',
    )
# post_save.connect(post_save_wishlist, sender=Wishlist)





@receiver(post_delete,sender=Wishlist)
def save_user_logs(sender,**kwargs):
    instance = kwargs["instance"] #<Wishlist: Potatoes>
    print("sender",sender.wishlist_user)
    userlogs_object, created = UserLogs.objects.get_or_create(
        userlogs_user=instance.wishlist_user,
        userlogs_action='wishlist_item_deleted'
    )