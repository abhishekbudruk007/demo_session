from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect , get_object_or_404, render
# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import  ListView
from .models import Wishlist , Order, OrderItem, Product,CheckoutAddress ,Payment
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from .forms import CheckoutForm
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_KEY
# @login_required
# def DetailView( request,pk):
#     product_fetched = Product.objects.filter(id=pk)[0]
#     context={
#         "object": product_fetched
#     }
#     return render(request,'products/product_detail_view.html',context)


class DetailViewCBV(DetailView):
    model = Product
    template_name = "products/product_detail_view.html"



def AddToWishlistFBV( request,pk):
    product_object = Product.objects.filter(id=pk)[0]

    wishlist_object ,created = Wishlist.objects.get_or_create(
        wishlist_user = request.user,
        wishlist_product=product_object
    )

    messages.success(request, 'Product Added to Wishlist')
    return redirect('dashboard:home')

import traceback
class WishListView(ListView):
    print("Inside ListView")
    template_name = 'products/wishlist.html'
    def get_queryset(self):
        query_set = Wishlist.objects.filter(wishlist_user=self.request.user)
        print("query_set",query_set)
        return query_set

class DeleteWishlistCBV(DeleteView):
    model = Wishlist
    success_url = reverse_lazy('products:wishlist')
    template_name = 'products/wishlist_confirm_delete.html'


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_product, created = OrderItem.objects.get_or_create(
        orderitem_product=product,
        orderitem_user=request.user,
        orderitem_ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.products.filter(orderitem_product__pk=product.pk).exists():
            order_product.orderitem_quantity += 1
            order_product.save()
            messages.info(request, "Added quantity Item")
            return redirect("products:product_detail_view", pk=pk)
        else:
            order.products.add(order_product)
            messages.info(request, "Item added to your cart")
            return redirect("products:product_detail_view", pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, "Item added to your cart")
        return redirect("products:product_detail_view", pk=pk)


def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(orderitem_product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                orderitem_product=product,
                orderitem_user=request.user,
                orderitem_ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \""+order_item.orderitem_product.product_name+"\" remove from your cart")
            return redirect("dashboard:home")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("products:product_detail_view", pk=pk)
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("products:product_detail_view", pk=pk)


def reduce_quantity_item(request, pk):
    product = get_object_or_404(Product, pk=pk )
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(orderitem_product__pk=product.pk).exists() :
            order_item = OrderItem.objects.filter(
                orderitem_product=product,
                orderitem_user=request.user,
                orderitem_ordered=False
            )[0]
            if order_item.orderitem_quantity > 1:
                order_item.orderitem_quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect("products:order_summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("products:order_summary")
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("products:order_summary")


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'products/order_summary.html', context)
        except ObjectDoesNotExist:
            # messages.error(self.request, "You do not have an order")
            return render(self.request, 'products/order_summary.html')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'products/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionaly for these fields
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()
                # if payment_option == 'C':
                #     order.payment = payment_option
                #     order.save()
                #     messages.add_message(self.request,messages.SUCCESS,"Ordered Successfully")
                #     return redirect('dashboard:home')
                # el
                if payment_option == 'S':
                    return redirect('products:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('products:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid Payment option")
                    return redirect('products:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("products:order_summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, "products/payment.html", context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total_price() * 100)  # cents

        try:
            # customer = stripe.Customer.create(
            #
            # )
            charge = stripe.Charge.create(
                amount=amount,
                currency="inr",
                source=token
            )

            # create payment
            payment = Payment()
            payment.stripe_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total_price()
            payment.save()

            # assign payment to order
            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Payment is Successful")
            return redirect('dashboard:home')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect('dashboard:home')

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "To many request error")
            return redirect('dashboard:home')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid Parameter")
            return redirect('dashboard:home')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Authentication with stripe failed")
            return redirect('dashboard:home')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect('dashboard:home')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong")
            return redirect('dashboard:home')

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request, "Not identified error")
            return redirect('dashboard:home')