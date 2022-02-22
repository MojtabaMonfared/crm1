from django.db import models
from django.contrib.auth.models import User


# Customer Model with basic information
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, verbose_name="نام کاربری")
    phone = models.CharField(max_length=200, null=True, verbose_name="تلفن تماس")
    email = models.CharField(max_length=200, null=True, verbose_name="ایمیل کاربر")
    profile_pic = models.ImageField(default="default.png", null=True, blank=True, verbose_name="تصویر پروفایل")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
 
    def __str__(self):
        return self.name

# Tag Model for products
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

# Product Model with additional information
class Product(models.Model):
    CATEGORY = (
        ('داخلی', 'داخلی'),
        ('خارجی', 'خارجی'),
    )
    name = models.CharField(max_length=200, null=True) 
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

# Users Orders Model with relationship to Customer and Products
class Order(models.Model):
    STATUS = (
        ('در حال بررسی', 'در حال بررسی'),
        ('سفارشات در مسیر تحویل', 'سفارشات در مسیر تحویل'),
        ('تحویل داده شده', 'تحویل داده شده'),
    )
    customer =models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    notes = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.product.name
