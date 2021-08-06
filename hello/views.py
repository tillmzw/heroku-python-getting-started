from django.conf import settings 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def host(request):
    return JsonResponse({"hostname": settings.HOST_NAME})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
