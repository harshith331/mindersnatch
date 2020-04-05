from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from mindapp.models import *
import datetime
from . import models
from time import timezone
from django.utils import timezone as t
import csv
from django.http import HttpResponse
from decouple import config


def activeTime(request):
    configuration = Config.objects.all().first()
    curr_time = t.now()
    if  request.user.is_staff:
        return 2  # for staff 
    if curr_time < configuration.start_time:
        return 1  # Contest hasnt started
    elif curr_time >= configuration.start_time and curr_time <= configuration.end_time:
        return 2  # Contest Active
    else:
        return 3  # Contest Ended


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        profile = user
        try:
            player = models.Player.objects.get(user=profile)
        except:
            player = models.Player(user=profile)
            player.timestamp = datetime.datetime.now()
            player.name = response.get('name')
            player.image = response.get('picture')
            player.email = response.get('email')
            player.save()
    elif backend.name == 'facebook':
        profile = user
        try:
            player = models.Player.objects.get(user=profile)
        except:
            player = models.Player(user=profile)
            player.name = response.get(
                'first_name')+" "+response.get('last_name')
            player.email = response.get('email')
            # print(response)
            player.image = "http://graph.facebook.com/%s/picture?type=large" \
                % response["id"]
            player.timestamp = datetime.datetime.now()
            player.save()


def saveLeaderboard(request):
    if request.GET.get("password") == config('LEADERBOARD_PASSWORD', cast=str):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="leaderboards.csv"'
        writer = csv.writer(response)
        for player in Player.objects.order_by("score", "timestamp"):
            writer.writerow([player.user.username, player.score])
        return response
    else:
        return HttpResponse("Not Authorised. Bad user :(")


def index(request):
    config=Config.objects.all().first()
    if activeTime(request) == 2:
        if request.user:
            if request.user.is_authenticated:
                try : 
                    player = Player.objects.get(user=request.user)
                    return render(request, 'index.html', {'user': player})
                except:
                    return render(request,'404.html',{'message':"Try Logging Again!!"})
        return render(request, 'index.html')
    elif activeTime(request) == 1:
        # Replace this with contest timer
        return render(request, 'timer.html',{'time':config.time})
    else:
        # Replace this with ended page
        return HttpResponse("Contest ended.")


@login_required(login_url="/")
def answer(request):
    config=Config.objects.all().first()
    cur_level=config.current_level
    tot_level=config.total_level
    player_check=Player.objects.get(user=request.user)
    if player_check.level <= tot_level:
        if player_check.level <=cur_level:
            if request.method == 'POST':
                try:
                    player = Player.objects.get(user=request.user)
                    try : 
                        past_sitn = Situation.objects.get(situation_no=player.current_sitn)
                        if past_sitn.sub == False:
                            op_no = request.POST.get('op_no')
                            try : 
                                option_c = option.objects.get(id=op_no)
                                if option_c.end:
                                    # player is dead redirect to start node
                                    player.current_sitn = Situation.objects.get(id=1).situation_no
                                    player.level=Situation.objects.get(id=1).level
                                    player.save()
                                    message = option_c.message
                                    return render(request, 'dead.html', {'player': player, 'message': message})
                                else:
                                    # option is non terminating one player progresses to next level
                                    player.current_sitn = option_c.next_sit
                                    player.score += 1
                                    player.timestamp = datetime.datetime.now()
                                    sitn = Situation.objects.get(situation_no=option_c.next_sit)
                                    player.level=sitn.level
                                    player.save()
                                    if player.level<= tot_level:
                                        if player.level <= cur_level:
                                            if sitn.sub == True:
                                                timer = SituationTimer.objects.get_or_create(player=player,situation=sitn)
                                                return render(request, 'subjective_level.html', {'player': player, 'sitn': sitn, 'timepassed':timer[0].timepassed()})
                                            else:
                                                return render(request, 'level.html', {'player': player, 'sitn': sitn})
                                        else:
                                            return HttpResponse("daily limit exceeded")
                                    else:
                                        return HttpResponse("player has won")
                            except : 
                                return render(request,'404.html',{'message':"Error getting Options!!"})
                        else:
                            ans = ""
                            ans = request.POST.get('ans')
                            timer = SituationTimer.objects.get_or_create(player=player, situation=past_sitn)
                            if past_sitn.checkAnswer(ans):
                                if player.level<= tot_level:
                                    if player.level <= cur_level:
                                        timer[0].end_time = datetime.datetime.now()
                                        timer[0].save()
                                        player.score += timer[0].timedifference()
                                        timer[0].delete()
                                        player.current_sitn = past_sitn.next_sitn
                                        player.timestamp = datetime.datetime.now()
                                        sitn = Situation.objects.get(situation_no=player.current_sitn)
                                        player.level=sitn.level
                                        player.save()
                                        if sitn.sub == True:
                                            new_timer = SituationTimer.objects.get_or_create(player=player, situation=sitn,
                                            start_time=datetime.datetime.now())
                                            return render(request, 'subjective_level.html', {'player': player, 'sitn': sitn ,'timepassed': new_timer[0].timepassed()})
                                        else:
                                            return render(request, 'level.html', {'player': player, 'sitn': sitn})
                                    else:
                                        return HttpResponse("daily limit exceeded")
                                else:
                                    return HttpResponse("player has won")
                            else:
                                messages.error(request, "Wrong Answer!, Try Again")
                                return render(request, 'subjective_level.html', {'player': player, 'sitn': past_sitn, 'timepassed':timer[0].timepassed()})
                    except : 
                        return render(request,'404.html',{'message':"Wait for new Situation!"})
                except:
                    return render(request,'404.html',{'message':"Try Logging in Again!!"})
            else:
                try :
                    player = Player.objects.get(user=request.user)
                    try : 
                        sitn = Situation.objects.get(situation_no=player.current_sitn)
                        if sitn.sub == True:
                            timer = SituationTimer.objects.get_or_create(
                                player=player, situation=sitn)
                            return render(request, "subjective_level.html", {'player': player, 'sitn': sitn, 'timepassed': timer[0].timepassed()})
                        else:
                            return render(request, "level.html", {'player': player, 'sitn': sitn})
                    except : 
                        return render(request,'404.html',{'message':"Wait for the new situation!!"})
                except : 
                    return render(request,'404.html',{'message':"Try Logging in Again!!"})
        
        else:
            # daily limit completed
            return HttpResponse("daily limit exceeded")
    else:
        #all situations covered
        return HttpResponse("player has won")



def leaderboard(request):
    players = Player.objects.all()
    context = {'players': players}
    if request.user:
        if request.user.is_authenticated:
            player = Player.objects.get(user=request.user)
            context['user'] = player
    return render(request, "leaderboard.html", context)


def rules(request):
    context = {}
    if request.user:
        if request.user.is_authenticated:
            player = Player.objects.get(user=request.user)
            context = {'user': player}
    return render(request, "rules.html", context)


def options(request):
    return render(request, "options.html")

def subjective(request):
    return render(request, "subjective.html")
