from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request
from django.contrib.auth import get_user

# Create your views here.

def index(request):
    return HttpResponse("Home Page" + str(get_user))


def sap(request):
    ss = "Hello"
    return HttpResponse(ss)


def send_otp(request):
    otp = get_user(request)
    return otp

