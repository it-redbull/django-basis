from django.contrib import messages
from django.shortcuts import redirect, render

def index(request):
    return render(request, 'pages/index.html', {
    })


def contact(request):
    return render(request, 'pages/contact.html')
