import os
import random

from django.conf import settings 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Greeting

# Create your views here.
def index(request):
    return JsonResponse({}) 


def host(request):
    try:
        lower_bound = int(os.environ.get("LOWER_RANDOM", 97))
        upper_bound = int(os.environ.get("UPPER_RANDOM", 97+25))
        randint = random.randint(lower_bound, upper_bound)
        random_char = chr(randint)
    except (TypeError, ValueError):
        random_char = "💩"
        
    return JsonResponse({
        "hostname": settings.HOST_NAME,
        "random_char": random_char 
    })


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
