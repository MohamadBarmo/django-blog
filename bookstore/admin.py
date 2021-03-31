from django.contrib import admin

# Register your models here.
from .models import Customer
from .models import Book
from .models import Order
from .models import Tag
#from .models import *

admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Tag)