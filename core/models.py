from django.db import models

from accounts.models import *
from payments.models import Transaction
          
class Category(models.Model):
    name = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(Vendor,on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    
    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, related_name="orderitems")
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey(Transaction, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.name
