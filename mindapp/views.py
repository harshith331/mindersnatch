from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from mindapp.models import Config
from . import models

# Create your views here.

def index(request):
    #Config for activating contest active and inactive time
    config = Config.objects.all().first()
    return render(request, 'index.html')
