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
    # sit1 = models.Situation.objects.get(id=1)

    print("-----------------------------")
    return render(request, 'index.html')

@login_required
def answer(request):
    if request.method == 'POST':
        op_no = request.POST.get('op_no')

    player=models.player.objects.get(user_id=request.user.pk)
    option=models.option.object.get(id=op_no)
    if option.end==True:
        #player is dead redirect to start node
        return render(request, 'dead.html',{'player':player})

    else:
        #option is non terminating one player progresses to next level
        player.current_sitn=option.next_sitn
        player.score+=1
        player.timestamp = datetime.datetime.now(tz=timezone.utc)
        sitn=models.Situation.object.get(situation_no=player.current_sitn)
        player.save()
        return render(request , 'level.html' ,{'player':player,'sitn':sitn})


