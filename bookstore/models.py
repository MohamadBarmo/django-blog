from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=100,null=True)
    age = models.CharField(max_length=100,null=True)
    avatar=models.ImageField(blank=True,null=True,default="profileimage.png")
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name 

class Tag (models.Model):
        name=models.CharField(max_length=100,null=True)
        def __str__(self):
            return self.name 
            
                   
class Book(models.Model):
        CATEGORY= (
        ('Classics','Classics'),
        ('Comic Book ','Comic Book '),
        ('Fantasy','Fantasy'),
        ('Horror','Horror'),
        )
        name=models.CharField(max_length=100,null=True)
        auther=models.CharField(max_length=100,null=True)
        price=models.FloatField(max_length=100,null=True)
        category=models.CharField(max_length=100,null=True, choices=CATEGORY)
        tag=models.ManyToManyField(Tag)
        description=models.CharField(max_length=200,null=True)
        date_created = models.DateTimeField(auto_now_add=True,null=True)

        def __str__(self):
            return self.name 
         


class Order(models.Model):
        STATUS= (
        ('Pending','Pending'),
        ('Delivered','Delivered'),
        ('Out of order','out of order'),
        ('in progress','in progress'),
        )
        customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
        book=models.ForeignKey(Book,null=True,on_delete=models.SET_NULL)
        tag=models.ManyToManyField(Tag)
        status=models.CharField(max_length=100,null=True , choices=STATUS)
        date_created = models.DateTimeField(auto_now_add=True,null=True)
        def __str__(self):
            return  self.status