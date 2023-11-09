from django.contrib import admin
from shoes.models import Order, Product
from rest_framework.authtoken.models import TokenProxy
admin.site.unregister(TokenProxy) # Hidden token section

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "stock", "get_price"]
    search_fields = ["name", "stock"]

    def get_price(self, obj):
        return "{:,} Dollar".format(obj.price)

    get_price.short_description = " Product's Price"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "status", "get_pr"]
    search_fields = ["user", "status"]

    def get_pr(self, obj):
        return "{:,} Dollar".format(obj.full_price)

    get_pr.short_description = "Total Orders  "
    #Add user and status and full price order