from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from accounts.models import Users
from shoes.models import Order, Product, OrderItem 
from rest_framework.authtoken.models import Token


class HomeView(View):
    def get(self, request):
        pro = Product.objects.all()
        count = 0
        if request.user.is_authenticated:
            basket = Order.get_basket(request.user)
            if basket:
                count = len(basket.orderitem_set.all())
        response = render(request, "products.html", {"products": pro, "count": count})
        if request.user.is_authenticated and not request.COOKIES.get("token", None):
            token, _ = Token.objects.get_or_create(user=request.user)
            response.set_cookie(key="token", value=token)
        return response
    

    def post(self, request):
        type = request.POST.get("type")

        if type == "reset":
            my_order = Order.objects.filter(user__id=request.user.id, status="1")
            my_order.update(status="2")
            return render(request, "products.html", {"products": Product.objects.all(), "count": 0})
        
        elif type == "add":
            id = request.POST.get("product-id")
            href = request.POST.get("href")
            my_order = Order.objects.filter(user__id=request.user.id, status="1")
            if request.user.is_authenticated:
                if my_order.exists():
                    my_order = my_order.get()
                    OrderItem.add(my_order, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                else:
                    basket = Order.create_basket(request.user)
                    OrderItem.add(basket, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                if href == "main":
                    return render(request, "products.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                else:
                    return render(request, "card.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": "{:,}".format(basket.full_price)})
        
        elif type == "remove":
            id = request.POST.get("product-id")
            href = request.POST.get("href")
            my_order = Order.objects.filter(user__id=request.user.id, status="1")
            if request.user.is_authenticated:
                if my_order.exists():
                    my_order = my_order.get()
                    OrderItem.remove(my_order, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                else:
                    basket = Order.create_basket(request.user)
                    OrderItem.remove(basket, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                if href == "main":
                    return render(request, "products.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                else:
                    return render(request, "card.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": "{:,}".format(basket.full_price)})

class CardView(View):
    def get(self, request):
        if request.user.is_authenticated:
            basket = Order.get_basket(request.user)
            if basket:
                order_items = basket.orderitem_set.all()
                return render(request, "card.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": "{:,}".format(basket.full_price)})
            else:
                return render(request, "card.html", {"basket": None, "items": None, "count": 0, "price": 0})
        else:
            return render(request, "card.html", {"basket": None, "items": None, "count": 0, "price":0})
            
    def post(self, request):
        type = request.POST.get("type")
        id = request.POST.get("product-id")
        href = request.POST.get("href")

        if type == "add":
            my_order = Order.objects.filter(user__id=request.user.id, status="1")
            if request.user.is_authenticated:
                if my_order.exists():
                    my_order = my_order.get()
                    OrderItem.add(my_order, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                else:
                    basket = Order.create_basket(request.user)
                    OrderItem.add(basket, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                if href == "main":
                    return render(request, "products.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                else:
                    return render(request, "card.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": "{:,}".format(basket.full_price)})
        
        elif type == "remove":
            my_order = Order.objects.filter(user__id=request.user.id, status="1")
            if request.user.is_authenticated:
                if my_order.exists():
                    my_order = my_order.get()
                    OrderItem.remove(my_order, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                else:
                    basket = Order.create_basket(request.user)
                    OrderItem.remove(basket, id, 1)
                    basket = Order.get_basket(request.user)
                    order_items = basket.orderitem_set.all()
                if href == "main":
                    return render(request, "products.html", {"products": Product.objects.all(), "count": len(basket.orderitem_set.all())})
                else:
                    return render(request, "card.html", {"basket": basket, "items": order_items, "count": len(basket.orderitem_set.all()), "price": "{:,}".format(basket.full_price)})
