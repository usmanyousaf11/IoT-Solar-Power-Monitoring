#!/bin/python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .models import crudinv, crudmodbus
from .forms import OrderForm, CreateUserForm, invform, mbform
from .filters import OrderFilter
from .filters import crudinvFilter
#from pymodbus.version import version
#from pymodbus.server.asynchronous import StartTcpServer
#from pymodbus.datastore import ModbusSequentialDataBlock
#from pymodbus.device import ModbusDeviceIdentification
#from pymodbus.datastore import ModbusSequentialDataBlock
#from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
#from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
#from django.core import serializers
#from django.conf import settings
import json
import datetime

# --------------------------------------------------------------------------- #
# import the twisted libraries we need
# --------------------------------------------------------------------------- #
from twisted.internet.task import LoopingCall

# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
@login_required(login_url='login')
def testrms1(request):
    # testvar1 = 222
    #a=5
    # return testvar1
    #run_updating_server()
    # results = crudinv.objects.all()
    # run_updating_server()
    # return render(request, "accounts/page1.html", {"crudinv": results})
    #v1,v2=updating_writer(a)
    text = "Currently, Inverter Parameters are:"
    val = 60
    time = 10
    test= 6
    currenttime = datetime.datetime.now()
    #register= register
    # address = 10
    content = {
        't1': text,
        'Add': time,
        'data': val,
        'test': test,
        'test2': currenttime,
        #'test3': testvar1,
    }
    return render(request, "accounts/page4.html", content)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    inverters = Order.objects.all()
    customers = Customer.objects.all()
    results = crudinv.objects.all()
    #aaa= crudinv.objects.get()
    #bbb= Order.objects.get()
    #ccc= aaa.entry_set.add(bbb)

    total_customers = customers.count()

    total_inverters = inverters.count()
    installed = inverters.filter(status='Installed').count()
    monitored = inverters.filter(status='Monitored').count()

    context = {
        'inverters': inverters,
        'customers': customers,
        'crudinv': results,
        'total_inverters': total_inverters,
        'monitored': monitored,
        'installed': installed,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def admin(request):
    return render(request, 'http://127.0.0.1:8000/admin/')

@login_required(login_url='login')
def multiplesearch(request):
    # invobj=crudinv.objects.raw('select * from crud_crudinv')
    results = crudinv.objects.all()
    # results = crudinv.objects.get(id=id)
    myFilter = crudinvFilter(request.GET, queryset=results)
    results = myFilter.qs
    # context = {'results':results}
    context = {'crudinv': results}
    # context = {'context1': context1, 'myFilter': myFilter}

    # return render(request, "search.html", {"crudinv": results})
    return render(request, "accounts/search.html", {"myFilter": myFilter, "crudinv": results})


@login_required(login_url='login')
def invdisplay(request):
    results = crudinv.objects.all()
    return render(request, "accounts/page1.html", {"crudinv": results}) 


@login_required(login_url='login')
def invinsert(request):
    if request.method == "POST":
        if request.POST.get('invname') and request.POST.get('invlocation') and request.POST.get('invsimnumber') and request.POST.get(
                'invclient') and request.POST.get('invstatus'):
            saveinv = crudinv()
            saveinv.invname = request.POST.get('invname')
            saveinv.invlocation = request.POST.get('invlocation')
            saveinv.invsimnumber = request.POST.get('invsimnumber')
            saveinv.invclient = request.POST.get('invclient')
            saveinv.invstatus = request.POST.get('invstatus')
            saveinv.save()
            messages.success(request, "The Record " + saveinv.invname + "is saved successfully..!")
            return render(request, "accounts/Create.html")
    else:
        return render(request, "accounts/Create.html")


@login_required(login_url='login')
def invinsert1(request):
    if request.method == "POST":
        if request.POST.get('name') and request.POST.get('phone') and request.POST.get(
                'email') and request.POST.get('date_created'):
            saveinv = Customer()
            saveinv.name = request.POST.get('name')
            saveinv.phone = request.POST.get('phone')
            saveinv.email = request.POST.get('email')
            saveinv.date_created = request.POST.get('date_created')
            saveinv.save()
            messages.success(request, "The Record " + saveinv.name + "is saved successfully..!")
            return render(request, "accounts/Create1.html")
    else:
        return render(request, "accounts/Create1.html")


@login_required(login_url='login')
def invedit(request, id):
    getinverterdetails = crudinv.objects.get(id=id)
    return render(request, 'accounts/edit.html', {"crudinv": getinverterdetails})


@login_required(login_url='login')
def invupdate(request, id):
    invupdate1 = crudinv.objects.get(id=id)
    form = invform(request.POST, instance=invupdate1)
    if form.is_valid():
        form.save()
        messages.success(request, "The Inverter record is updated successfully...!")
        return render(request, 'accounts/edit.html', {"crudinv": invupdate1})


@login_required(login_url='login')
def invdel(request, id):
    delinverter = crudinv.objects.get(id=id)
    delinverter.delete()
    results = crudinv.objects.all()
    return render(request, "accounts/page2.html", {"crudinv": results})


@login_required(login_url='login')
def mbdisplay(request):
    results2 = crudmodbus.objects.all()
    customer = Customer.objects.all()
    context = {'customer': customer, 'crudmodbus': results2}
    return render(request, "accounts/page2.html", context)


@login_required(login_url='login')
def mbinsert(request):
    if request.method == "POST":
        if request.POST.get('mbid') and request.POST.get('mbinputvoltage') and request.POST.get(
                'mbinputcurrent') and request.POST.get('mboutputvoltage') and request.POST.get(
            'mboutputcurrent') and request.POST.get('mboutputpower'):
            savemb = crudmodbus()
            savemb.mbid= request.POST.get('mbid')
            savemb.mbinputvoltage = request.POST.get('mbinputvoltage')
            savemb.mbinputcurrent = request.POST.get('mbinputcurrent')
            savemb.mboutputvoltage = request.POST.get('mboutputvoltage')
            savemb.mboutputcurrent = request.POST.get('mboutputcurrent')
            savemb.mboutputpower = request.POST.get('mboutputpower')
            savemb.save()
            messages.success(request, "The Record " + save.mbid + "is saved successfully..!")
            return render(request, "accounts/Create2.html")
    else:
        return render(request, "accounts/Create2.html")


@login_required(login_url='login')
def mbedit(request, id):
    getsitedetails = crudmb.objects.get(id=id)
    return render(request, 'accounts/edit2.html', {"crudmb": getsitedetails})


@login_required(login_url='login')
def mbupdate(request, id):
    mbupdate = crudmb.objects.get(id=id)
    form = mbform(request.POST, instance=mbupdate)
    if form.is_valid():
        form.save()
        messages.success(request, "The site record is updated successfully...!")
        return render(request, 'accounts/edit2.html', {"crudmb": mbupdate})


@login_required(login_url='login')
def mbdel(request, id):
    delsite = crudmb.objects.get(id=id)
    delsite.delete()
    results2 = crudmb.objects.all()
    return render(request, "accounts/page2.html", {"crudmb": results2})


@login_required(login_url='login')
def webpage3(request):
    return render(request, "accounts/page3.html")


@login_required(login_url='login')
def webtestp(request):
    return render(request, "accounts/Test.py")


@login_required(login_url='login')
def webtestrms1(request):
    return render(request, "accounts/RMS1.py")


@login_required(login_url='login')
def webtestrms2(request):
    return render(request, "accounts/RMS2.py")


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def customer1(request, pk_test1):
    #customer1 = crudinv.objects.get(id=pk_test1)

    #orders1 = customer1.order_set.all()
    #order_count1 = orders1.count()

    #myFilter1 = OrderFilter(request.GET, queryset=orders1)
    #orders1 = myFilter1.qs

    #context = {'customer1': customer1}
    #return render(request, 'accounts/customer1.html', context)
    results = crudinv.objects.all()
    return render(request, "accounts/customer1.html", {"crudinv": results})


@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
