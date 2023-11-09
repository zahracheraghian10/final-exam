from django.db import models
from accounts.models import Users 

class Product(models.Model):
    name = models.CharField(max_length=99, verbose_name="Product's Name ")
    image = models.ImageField(verbose_name=" Product's image", null=True, blank=True)
    stock = models.PositiveIntegerField( default=0)
    price = models.PositiveBigIntegerField()

    # class Meta:
    #     verbose_name = "محصول"
    #     verbose_name_plural = "محصول ها"

    # def __str__(self):
    #     return self.name
        
class Order(models.Model):

    STATUS_CHOICES = (("1", " Cart"),("2", "Paying  "),("3", " Cancelled"),)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES)
    full_price = models.PositiveBigIntegerField(
        verbose_name=" Total Price ", default=0)
        
    @classmethod
    def get_basket(cls, user):
        basket = cls.objects.filter(user=user.id, status="1")
        if basket.exists():
            return basket.get()
        return None

    @classmethod
    def create_basket(cls, user):
        my_basket = cls(
            user=user,
            status=1
        )
        my_basket.save()
        return my_basket
    
    #Add Update_price for calcuting Full Price
    def update_price(self):
        order_items = self.orderitem_set.all()
        fprice = 0
        for i in order_items:
            fprice += i.product.price * i.product_count
        self.full_price = fprice
        self.save()

    def __str__(self):
        return str(self.user)
    
        
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Order")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Product")
    product_price = models.PositiveBigIntegerField(verbose_name="Product's Price ")
    product_count = models.IntegerField(verbose_name="Product's Number ")

    @classmethod
    def add(cls, order, product, count):
        prod = Product.objects.get(pk=product)
        data = cls.objects.filter(order=order, product__id=product)
        if data.exists():
            my_order_item = data.get()
            my_order_item.product_price = my_order_item.product.price
            my_order_item.product_count = my_order_item.product_count + 1
            my_order_item.save()
            my_order_item.order.update_price()
            return True
        else:
            instance = cls(order=order, product_price=prod.price,
                        product=prod, product_count=count)
            instance.save()
            instance.order.update_price()
            return True

    @classmethod
    def remove(cls, order, product, count):
        data = cls.objects.filter(order=order, product__id=product)
        if data.exists():
            my_order_item = data.get()
            if my_order_item.product_count - count <= 0:
                target_order = my_order_item.order
                my_order_item.delete()
                target_order.update_price()
                return True
            else:
                my_order_item.product_count -= count
                my_order_item.save()
                my_order_item.order.update_price()
                return True
        else:
            return False
