import datetime

from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Filter_Price(models.Model):
    FILTER_PRICE =(
        ('1000 To 10000', '1000 To 10000'),
        ('2000 To 20000', '2000 To 20000'),
        ('3000 To 30000', '3000 To 30000'),
        ('4000 To 40000', '4000 To 40000'),
        ('5000 To 50000', '5000 To 50000'),
    )

    price = models.CharField(choices=FILTER_PRICE, max_length=60)

    def __str__(self):
        return self.price


class Product(models.Model):
    CONDITION = (('New','New'),('Old','Old'))
    STOCK = ('IN STOCK','IN STOCK'),('OUT OF STOCK','OUT OF STOCK')
    STATUS = ('Publish','Publish'),('Draft','Draft')

    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='Product_images/img')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION, max_length=100)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK, max_length=200)
    status = models.CharField(choices=STATUS, max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    categories = models.ForeignKey(Categories,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_Price,on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('75%Y%m%d23') + str(self.id)
        return super().save(*args,**kwargs)

    def __str__(self):
        return self.name


class Images(models.Model):
    image = models.ImageField(upload_to='Product_images/img')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField(max_length=10)
    phone = models.IntegerField(max_length=15)
    email = models.EmailField(max_length=100)
    additional_info = models.TextField(blank=True,null=True)
    amount = models.IntegerField()
    payment_id = models.CharField(max_length=300, null=True,blank=True)
    paid = models.BooleanField(null=True,default=False)
    date = models.DateTimeField(default=datetime.datetime.today)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to="Product_images/Order_Img")
    quantity = models.CharField(max_length=28)
    price = models.CharField(max_length=500)
    total = models.CharField(max_length=1000)

    def __str__(self):
        return self.order.user.username




