from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def share_view(request, share_name):
    print(request)
    return HttpResponse('Mounted ' + share_name)
