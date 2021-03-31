from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
from django.forms import  ModelForm
from .forms import OrderForm,CreateNewUSer , CustomerForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.contrib.auth import authenticate ,logout
from django.contrib.auth import  login as mylogin
from django.contrib.auth.decorators import  login_required
from .decorators import  notLoggedUsers,allowedUsers,forAdmins
from django.contrib.auth.models import Group

import requests
from django.conf import settings


@login_required(login_url="login")
#@allowedUsers(allowedgroups=["admin"])
@forAdmins
def home(request):
      #return HttpResponse('home page')
   
    customers=Customer.objects.all()
    orders=Order.objects.all()
    t_orders=orders.count()
    d_orders=orders.filter(status='Delivered').count()
    p_orders=orders.filter(status='Pending').count()
    o_orders=orders.filter(status='Out of order').count()
    i_orders=orders.filter(status='in progress').count()
    context = {'customers':customers,
    'orders':orders,
    't_orders':t_orders,
    'p_orders':p_orders,
    'd_orders':d_orders,
    'i_orders':i_orders,
    'o_orders':o_orders
    }
    return render(request,'bookstore/dashboard.html',context)

@login_required(login_url="login")
@forAdmins
def books(request):
     # return HttpResponse('users page')
    allbooks=Book.objects.all()
    return render(request,'bookstore/books.html', {'allbooks': allbooks})

@login_required(login_url="login")
def customer(request,PK):
    #  return HttpResponse('about page')
    customer= Customer.objects.get(id = PK)
    orders=customer.order_set.all()
    Orders_Numbers=customer.order_set.count()
    context = {'customer':customer,
    'orders':orders,
    'Orders_Numbers':Orders_Numbers
     }
    return render(request,'bookstore/customer.html',context)

#def create(request):
   # form=OrderForm()
    #if request.method =='POST':
      # # print(request.POST)
      # form = OrderForm(request.POST)
   # if form.is_valid():
    #   form.save()
    #   return redirect('/')
  #  context={'form':form}
   # return render(request,'bookstore/my_order_form.html', context)

@login_required(login_url="login")
@allowedUsers(allowedgroups=["admin"])
def create(request,PK):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('book','status'),extra=8)
    customer=Customer.objects.get(id=PK)
    formset=OrderFormSet( queryset=Order.objects.none(), instance=customer)
    form=OrderForm()
    if request.method =='POST':
       # print(request.POST)
      # form = OrderForm(request.POST)
       formset=OrderFormSet(request.POST,instance=customer)
    if formset.is_valid():
       formset.save()
       return redirect('/')
    context={'formset':formset}
    return render(request,'bookstore/my_order_form.html', context)

@login_required(login_url="login")
@allowedUsers(allowedgroups=["admin"])
def update(request,PK):
    order=Order.objects.get(id=PK)
    form=OrderForm(instance=order)
    if request.method =='POST':
       # print(request.POST)
       form = OrderForm(request.POST,instance=order)
    if form.is_valid():
       form.save()
       return redirect('/')
    context={'form':form}
    return render(request,'bookstore/my_order_form.html', context)

@login_required(login_url="login")
@allowedUsers(allowedgroups=["admin"])
def delete(request,PK):
    order=Order.objects.get(id=PK)
    if request.method =='POST':
       order.delete()
       return redirect('/')
    context={'order':order}
    return render(request,'bookstore/delete_form.html', context)


#def login(request):
 #  if request.user.is_authenticated
  #   return redirect ("home")
  #  context={}
 #   return render(request,'bookstore/login.html', context)
@notLoggedUsers
def register(request):
   #if request.user.is_authenticated:
   #    return redirect ("home")
  # else:
         form=UserCreationForm()
         if request.method =='POST':
            form=UserCreationForm(request.POST)
            if form.is_valid():
               recaptcha_response=request.POST.get('g-recaptcha-response')
               data={
                  'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                  'response' : recaptcha_response
               }
               r=requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
               resut=r.json()
               if resut['success']:
                  user=form.save()
                  username=form.cleaned_data.get('username')
                  #group=Group.objects.get(name='customer')
                  #user.groups.add(group)
                  messages.success(request,username + ' created successfully !')
                  return redirect('login')
               else :
                     messages.error(request, ' Invalid recaptcha.Please try again !')

              
              
              
         context={'form':form}
         return render(request,'bookstore/register.html', context)

@notLoggedUsers
def userlogin(request):
   
      if request.method =='POST':
         username =request.POST.get("username")
         password =request.POST.get("password")
         user=authenticate(request,username=username,password=password)
         if user is not None:
            mylogin(request,user)
            return redirect('home')
         else:
            messages.info(request,"Credential error")
      context={}
      return render(request,'bookstore/login.html', context)


def userlogout(request):
   logout(request)
   return redirect('login')

@login_required(login_url="login")
@allowedUsers(allowedgroups=["customer"])
def userprofile(request):
   #customer= Customer.objects.get(id = PK)
   orders=request.user.customer.order_set.all()
   #Orders_Numbers=customer.order_set.count()
   t_orders=orders.count()
   d_orders=orders.filter(status='Delivered').count()
   p_orders=orders.filter(status='Pending').count()
   i_orders=orders.filter(status='in progress ').count()
   o_orders=orders.filter(status='Out of order').count()
   context = {
   'orders':orders,
   't_orders':t_orders,
   'p_orders':p_orders,
   'd_orders':d_orders,
   'i_orders':i_orders,
   'o_orders':o_orders
   }
  # context={'orders':orders}
   return render(request,'bookstore/profile.html', context)


@login_required(login_url="login")

def profileinfo(request):
   customer=request.user.customer
   form=CustomerForm(instance=customer)
   if request.method =='POST':
      form=CustomerForm(request.POST,request.FILES,instance=customer)
      if form.is_valid:
         form.save()



   context = {
  'form':form
   }
  # context={'orders':orders}
   return render(request,'bookstore/profile_info.html', context)
   