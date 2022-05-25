from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def indexView(request):
    return HttpResponse("Index of the client side")