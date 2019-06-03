from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import Http404
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .models import Transaction
import json
from datetime import timedelta, datetime
a = datetime.now() - timedelta(days = 30)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum

@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def book(request, *args, **kwargs):
    
    
    user = request.user

    gallons_pumped_total = Transaction.objects.filter(customer=user).aggregate(Sum("gallons_pumped"))
    gross_amount_total = Transaction.objects.filter(customer=user).aggregate(Sum("gross_amount"))
    net_amount_total = Transaction.objects.filter(customer=user).aggregate(Sum("net_amount"))
    discount_on_fuel_total = Transaction.objects.filter(customer=user).aggregate(Sum("discount_on_fuel"))

    total_dict = {
        "gallons_pumped_total":gallons_pumped_total,
        "gross_amount_total":gross_amount_total,
        "net_amount_total":net_amount_total,
        "discount_on_fuel_total":discount_on_fuel_total
    }

    objects = Transaction.objects.filter(customer=user,
    purchased_date__gte=datetime.date(a))
    transaction_dicts = []
    if objects.exists():
        for obj in objects:
            new_dict = {
                "customer":obj.customer.username,
                "truck_number":obj.truck_number,
                "purchased_date":obj.purchased_date,
                "base_price":obj.base_price,
                "plus_fees":obj.plus_fees,
                "net_price":obj.net_price,
                "pump_price":obj.pump_price,
                "discount":obj.discount,
                "gallons_pumped":obj.gallons_pumped,
                "gross_amount":obj.gross_amount,
                "net_amount":obj.net_amount,
                "discount_on_fuel":obj.discount_on_fuel
            }
            transaction_dicts.append(new_dict)
    return Response(status=status.HTTP_200_OK, data={"data":transaction_dicts, "total":total_dict})


@csrf_exempt
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/signup.html', {
        'form':form
    })

class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        print(request.user)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK, data={"data": "Token has been deleted"})