import csv
from django.http.response import JsonResponse
from django.urls.conf import path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from mindapp.models import *
from time import process_time, timezone
from django.utils import timezone as t
from django.http import HttpResponse
from decouple import config
from graphviz import Graph
import graphviz
curr_leaderboard = None

# Helper functions -------------/


def activeTime(request):
    configuration = Config.objects.all().first()
    curr_time = t.now()
    if request.user.is_staff or curr_time >= configuration.start_time and curr_time <= configuration.end_time:
        return 2  # for staff or Contest Active
    elif curr_time < configuration.start_time:
        return 1  # Contest hasnt started
    else:
        return 3  # Contest Ended


def isFrozen():
    return t.now() >= Config.objects.all().first().freeze_time


def updateLeaderboard():
    global curr_leaderboard
    if not isFrozen():
        curr_leaderboard = Player.objects.all().order_by('-level', 'score', 'timestamp')
        return curr_leaderboard
    return curr_leaderboard


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        profile = user
        try:
            player = Player.objects.get(user=profile)
        except:
            player = Player(user=profile)
            player.timestamp = t.now()
            player.name = response.get('name')
            player.image = response.get('picture')
            player.email = response.get('email')
            player.save()

    elif backend.name == 'github':
        profile = user
        try:
            player = Player.objects.get(user=profile)
        except:
            player = Player(user=profile)
            player.timestamp = t.now()
            player.name = response.get('name')
            player.image = response.get('avatar_url')
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
            player.timestamp = t.now()
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


def ans_post(request, cur_level, tot_level):
    """ Handling Post requests while answering """

    try:
        player = Player.objects.get(user=request.user)
        past_sitn = Situation.objects.get(situation_no=player.current_sitn)
        if past_sitn.sub == False:
            op_no = request.POST.get('op_no')
            option_c = option.objects.get(id=op_no)

            if option_c.end:
                # player is dead redirect to start node
                player.current_sitn = Situation.objects.get(
                    situation_no=1).situation_no
                player.level = Situation.objects.get(situation_no=1).level
                player.score += 1

                # Activate the graph feature
                player.completed_or_dead = True

                player.save()
                updateLeaderboard()
                message = option_c.message
                return render(request, 'dead.html', {'user': player, 'message': message})
            else:
                # option is non terminating one player progresses to next level
                player.current_sitn = option_c.next_sit
                player.score += 1
                player.timestamp = t.now()
                sitn = Situation.objects.get(situation_no=option_c.next_sit)
                player.level = sitn.level

                # Appending the next situation to the visited string
                player.visited_nodes += f"{sitn.situation_no} "

                player.save()
                updateLeaderboard()
                if player.level <= tot_level and player.level <= cur_level:
                    if sitn.sub == True:
                        timer = SituationTimer.objects.get_or_create(
                            player=player, situation=sitn)
                        return render(request, 'subjective_level.html', {'user': player, 'sitn': sitn, 'timepassed': timer[0].timepassed()})
                    else:
                        return render(request, 'level.html', {'user': player, 'sitn': sitn, 'options': options})
                elif player.level <= tot_level and player.level > cur_level:
                    return render(request, "pls_wait.html", {'user': player})
                else:
                    messg = Situation.objects.get(
                        situation_no=player.current_sitn).text
                    return render(request, "finish.html", {'user': player, 'messg': messg})
        else:
            ans = ""
            ans = request.POST.get('ans')
            timer = SituationTimer.objects.get_or_create(
                player=player, situation=past_sitn)
            if past_sitn.checkAnswer(ans):
                timer[0].end_time = t.now()
                timer[0].save()
                player.score += timer[0].timedifference()
                timer[0].delete()
                player.current_sitn = past_sitn.next_sitn
                player.timestamp = t.now()
                sitn = Situation.objects.get(situation_no=player.current_sitn)
                player.level = sitn.level

                # Appending the next situation to the visited string
                player.visited_nodes += f"{sitn.situation_no} "

                player.save()
                updateLeaderboard()
                if player.level <= tot_level and player.level <= cur_level:
                    if sitn.sub == True:
                        new_timer = SituationTimer.objects.get_or_create(player=player, situation=sitn,
                                                                         start_time=t.now())
                        return render(request, 'subjective_level.html', {'user': player, 'sitn': sitn, 'timepassed': new_timer[0].timepassed()})
                    else:
                        options = sitn.options.all()
                        return render(request, 'level.html', {'user': player, 'sitn': sitn,'options' : options})
                elif player.level <= tot_level and player.level > cur_level:
                    return render(request, "pls_wait.html", {'user': player, })
                else:
                    messg = Situation.objects.get(
                        situation_no=player.current_sitn).text
                    return render(request, "finish.html", {'user': player, 'messg': messg})
            else:
                return render(request, 'subjective_level.html', {'user': player, 'sitn': past_sitn, 'timepassed': timer[0].timepassed(), 'status': 302, })
    except:
        return render(request, '404.html')


def ans_nonpost(request):
    """ Handling requests other than post while answering """
    try:
        player = Player.objects.get(user=request.user)
        sitn = Situation.objects.get(situation_no=player.current_sitn)
        print("visited !!!!")
        print(sitn.situation_no)
        player.visited_nodes += f"{sitn.situation_no} "
        player.save()

        if sitn.sub == True:
            timer = SituationTimer.objects.get_or_create(
                player=player, situation=sitn)
            return render(request, "subjective_level.html", {'user': player, 'sitn': sitn, 'timepassed': timer[0].timepassed()})
        else:
            options = sitn.options.all()
            for option in options:
                print(option.text)
            return render(request, "level.html", {'user': player, 'sitn': sitn, 'options': options})
    except Exception as e:
        print(e)
        return render(request, '404.html')

# Page functions -------------/



def index(request):
    config = Config.objects.all().first()
    if activeTime(request) == 2:
        if request.user and request.user.is_authenticated:
            try:
                frozen = isFrozen()
                player = Player.objects.get(user=request.user)
                return render(request, 'index.html', {'user': player, 'frozen': frozen})
            except Exception as e:
                print(e)
                return render(request, '404.html', {'message': "Try Logging Again!!"})
        return render(request, 'index.html')
    elif activeTime(request) == 1:
        if request.user and request.user.is_authenticated:
            player = Player.objects.get(user=request.user)
            return render(request, 'timer.html', {'time': config.time, 'user': player})
        return render(request, 'timer.html', {'time': config.time})
    else:
        return render(request, 'cont_end.html')


@login_required(login_url="/")
def answer(request):
    config = Config.objects.all().first()
    cur_level = config.current_level
    tot_level = config.total_level
    player_check = Player.objects.get(user=request.user)
    if activeTime(request) == 2:
        if player_check.level <= tot_level and player_check.level <= cur_level:
            if request.method == 'POST':
                return ans_post(request, cur_level, tot_level)
            else:
                return ans_nonpost(request)
        elif player_check.level <= tot_level and player_check.level > cur_level:
            # daily limit completed
            return render(request, "pls_wait.html", {'user': player_check, })
        else:
            # all situations covered
            messg = Situation.objects.get(
                situation_no=player_check.current_sitn).text
            return render(request, "finish.html", {'user': player_check, 'messg': messg})
    elif activeTime(request) == 1:
        return render(request, 'timer.html', {'time': config.time})
    else:
        return render(request, 'cont_end.html')


@login_required(login_url="/")
def leaderboard(request):
    config = Config.objects.all().first()
    if activeTime(request) == 2 or activeTime(request) == 3:
        players = updateLeaderboard()
        context = {'players': players}
        if request.user and request.user.is_authenticated:
            player = Player.objects.get(user=request.user)
            context['user'] = player
        return render(request, "lboard.html", context)
    else:
        return render(request, 'timer.html', {'time': config.time})


@login_required(login_url="/")
def rules(request):
    config = Config.objects.all().first()
    if activeTime(request) == 2 or activeTime(request) == 3:
        context = {}
        if request.user and request.user.is_authenticated:
            player = Player.objects.get(user=request.user)
            context = {'user': player}
        return render(request, "rules.html", context)
    else:
        return render(request, 'timer.html', {'time': config.time})


def rule(request):
    return render(request, "rules_page.html")


def logout_view(request):
    logout(request)
    return redirect(index)


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def privacy_policy_fb(request):
    return render(request, "privacypolicy.html")


@login_required(login_url="/")
def graph_and_player_path(request):
    player = Player.objects.get(user=request.user)

    if player.completed_or_dead == False:
        return JsonResponse({})
    # visited nodes of the current player
    visited = player.visited_nodes.split(" ")[0: -1]

    # creating the graph based on the database
    situations = Situation.objects.all().order_by("situation_no")
    graph = {}

    for situation in situations:
        graph[situation.situation_no] = []

    for situation in situations:
        if situation.sub == True:
            # Situation has a subjective answer
            graph[situation.situation_no].append(str(situation.next_sitn))

        else:
            # There are options to choose from
            options = situation.options.all()
            for option in options:
                print(option.text, option.end)
                if not option.end:
                    graph[situation.situation_no].append(str(option.next_sit))

    data = {
        'visited': visited,
        'graph': graph,
    }

    response = JsonResponse(data)
    print(response.content)
    return JsonResponse(data)


@login_required(login_url="/")
def graph(request):
    player = Player.objects.get(user=request.user)
    if player.completed_or_dead == True:
        return render(request, "graph.html")
    return redirect("/")

@login_required(login_url="/")
def graphy(request):
    player = Player.objects.get(user=request.user)
    if player.completed_or_dead == False:
        return redirect("/")
    visited = player.visited_nodes.split(" ")[0: -1]
    graph = graphviz.Digraph(format='svg')
    situations = Situation.objects.all()
    for situation in situations:
        if situation.sub == True:
            j=str(situation.situation_no)
            i=str(situation.next_sitn)
            graph.edge(j,i,color='#A9EAA9',fillcolor='#A9EAA9', style='filled')
        else:
            options = situation.options.all()
            for option in options:
                print(option.text, option.end)
                if not option.end:
                    i=str(situation.situation_no)
                    j=str(option.next_sit)
                    graph.edge(i,j,color='#A9EAA9',fillcolor='#A9EAA9', style='filled')
        graph.node(str(situation.situation_no),color='white', fontcolor='black',fillcolor='white', style='filled')
    print(visited)
    for v in visited:
        sitn = Situation.objects.get(situation_no=v)
        text = sitn.text
        graph.node(v,color='#A9EAA9',fillcolor='#A9EAA9', style='filled',tooltip=text, fontcolor='black')
    graph = graph.pipe().decode('utf-8')
    return render(request,"graphy.html",{ 'graph': graph })