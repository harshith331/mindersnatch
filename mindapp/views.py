from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from mindapp.models import *
import datetime
from . import models
from time import timezone
from django.utils import timezone as t
import csv
from django.http import HttpResponse
from decouple import config
import sys

curr_leaderboard = None

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

def isFrozen():
    return t.now() >= Config.objects.all().first().freeze_time

def updateLeaderboard():
    global curr_leaderboard
    if not isFrozen():
        curr_leaderboard = Player.objects.all().order_by('-level','score','timestamp')
        return curr_leaderboard
    return curr_leaderboard

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
        for player in updateLeaderboard():
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
                    frozen = isFrozen()
                    player = Player.objects.get(user=request.user)
                    return render(request, 'index.html', {'user': player, 'frozen' : frozen})
                except Exception as e:
                    return render(request,'404.html',{'message':"Try Logging Again!!"})
        return render(request, 'index.html')
    elif activeTime(request) == 1:
        if request.user:
            if request.user.is_authenticated:
                player = Player.objects.get(user=request.user)
                return render(request, 'timer.html', {'time':config.time, 'user':player})
        return render(request, 'timer.html',{'time':config.time})
    else:
        return render(request, 'cont_end.html')


@login_required(login_url="/")
def answer(request):
    config = Config.objects.all().first()
    cur_level = config.current_level
    tot_level = config.total_level
    player_check = Player.objects.get(user=request.user)
    if activeTime(request) == 2:
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
                                        player.current_sitn = Situation.objects.get(situation_no=1).situation_no
                                        player.level=Situation.objects.get(situation_no=1).level
                                        player.score +=1
                                        player.save()
                                        updateLeaderboard()
                                        message = option_c.message
                                        return render(request, 'dead.html', {'user': player, 'message': message})
                                    else:
                                        # option is non terminating one player progresses to next level
                                        player.current_sitn = option_c.next_sit
                                        player.score += 1
                                        player.timestamp = datetime.datetime.now()
                                        sitn = Situation.objects.get(situation_no=option_c.next_sit)
                                        player.level=sitn.level
                                        player.save()
                                        updateLeaderboard()
                                        if player.level<= tot_level:
                                            if player.level <= cur_level:
                                                if sitn.sub == True:
                                                    timer = SituationTimer.objects.get_or_create(player=player,situation=sitn)
                                                    return render(request, 'subjective_level.html', {'user': player, 'sitn': sitn, 'timepassed':timer[0].timepassed()})
                                                else:
                                                    return render(request, 'level.html', {'user': player, 'sitn': sitn})
                                            else:
                                                return render(request,"pls_wait.html",{'user': player,})
                                        else:
                                            messg=Situation.objects.get(situation_no=player.current_sitn).text
                                            return render(request,"finish.html",{'user': player,'messg':messg})
                                except : 
                                    return render(request,'404.html')
                            else:
                                ans = ""
                                ans = request.POST.get('ans')
                                timer = SituationTimer.objects.get_or_create(player=player, situation=past_sitn)
                                if past_sitn.checkAnswer(ans):
                                    timer[0].end_time = datetime.datetime.now()
                                    timer[0].save()
                                    player.score += timer[0].timedifference()
                                    timer[0].delete()
                                    player.current_sitn = past_sitn.next_sitn
                                    player.timestamp = datetime.datetime.now()
                                    sitn = Situation.objects.get(situation_no=player.current_sitn)
                                    player.level=sitn.level
                                    player.save()
                                    updateLeaderboard()
                                    if player.level<= tot_level:
                                        if player.level <= cur_level:
                                            if sitn.sub == True:
                                                new_timer = SituationTimer.objects.get_or_create(player=player, situation=sitn,
                                                start_time=datetime.datetime.now())
                                                return render(request, 'subjective_level.html', {'user': player, 'sitn': sitn ,'timepassed': new_timer[0].timepassed()})
                                            else:
                                                return render(request, 'level.html', {'user': player, 'sitn': sitn})
                                        else:
                                            return render(request,"pls_wait.html",{'user': player,})
                                    else:
                                        messg=Situation.objects.get(situation_no=player.current_sitn).text
                                        return render(request,"finish.html",{'user': player,'messg':messg})
                                else:
                                    return render(request, 'subjective_level.html', {'user': player, 'sitn': past_sitn, 'timepassed':timer[0].timepassed(), 'status':302,})
                        except : 
                            return render(request,'404.html')
                    except:
                        return render(request,'404.html')
                else:
                    try :
                        player = Player.objects.get(user=request.user)
                        try : 
                            sitn = Situation.objects.get(situation_no=player.current_sitn)
                            if sitn.sub == True:
                                timer = SituationTimer.objects.get_or_create(
                                    player=player, situation=sitn)
                                return render(request, "subjective_level.html", {'user': player, 'sitn': sitn, 'timepassed': timer[0].timepassed()})
                            else:
                                return render(request, "level.html", {'user': player, 'sitn': sitn})
                        except : 
                            return render(request,'404.html')
                    except : 
                        return render(request,'404.html')
            else:
                # daily limit completed
                return render(request,"pls_wait.html",{'user': player_check,})
        else:
            #all situations covered
            messg=Situation.objects.get(situation_no=player_check.current_sitn).text
            return render(request,"finish.html",{'user': player_check,'messg':messg})
    elif activeTime(request) == 1:
        return render(request, 'timer.html',{'time':config.time})
    
    else:
        return render(request, 'cont_end.html')


@login_required(login_url="/")
def leaderboard(request):
    config = Config.objects.all().first()
    if activeTime(request) == 2 or activeTime(request) == 3:
        players = updateLeaderboard()
        context = {'players': players}
        if request.user:
            if request.user.is_authenticated:
                player = Player.objects.get(user=request.user)
                context['user'] = player
        return render(request, "lboard.html", context)
    else:
        return render(request, 'timer.html',{'time':config.time})

@login_required(login_url="/")
def rules(request):
    config = Config.objects.all().first()
    if activeTime(request) == 2 or activeTime(request) == 3:
        context = {}
        if request.user:
            if request.user.is_authenticated:
                player = Player.objects.get(user=request.user)
                context = {'user': player}
        return render(request, "rules.html", context)
    else:
        return render(request, 'timer.html',{'time':config.time})

def rule(request):
    return render(request, "rules_page.html")

def logout_view(request):
    logout(request)
    return redirect(index)

def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)

def privacy_policy_fb(request):
    return render(request,"privacypolicy.html")