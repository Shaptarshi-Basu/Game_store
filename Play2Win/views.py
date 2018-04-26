from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from .forms import UserForm,AddGameForm
from .models import *
import json
import operator
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

class UserFormView(View):
    form_class = UserForm
    template='templates/registration.html'

    #display blank form
    def get(self,request):
        form = UserForm()
        return render(request, 'registration.html', {'form': form})
    """
    This method is effectively used when we submit the registration form.
    check if the form is valid and then extract the email ,name.The player model is populated, mail sent to the
    corresponding user email.
    """
    def post(self,request):
        form = UserForm(request.POST)
        if form.is_valid():
            userDatabase = form.save(commit=False)
            name = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            if not name.isalpha():
                return render(request, 'registration.html', {'form': form, 'msg':"Use only alpha numeric"})
            user = authenticate(username=name, password=raw_password)
            dev = request.POST.get("developer", "not_developer") == "isDeveloper"  # check if its a developer or player
            userDatabase.developer = dev
            userDatabase.save()
            player = Player.objects.create(user=userDatabase, developer=dev, activated=False)
            hashed_password = userDatabase.password
            sendMailToUser(name, hashed_password, email)
            return redirect('/login')
        else:
            return render(request, 'registration.html', {'form': form})

            #return user object if it has been created
            user =authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('index.html')
            #return render(request, self.template_name,{'dashboard' : })
            return render(request, 'index.html')
def sendMailToUser(name, pw, email):
    secure_link = name + "$$$$" + pw
    msg = """
Dear %(name)s,

Thanks for registering to Play2Win Store

Thanks and Regards,
Shaptarshi Basu!
https://aqueous-reaches-38143.herokuapp.com/dashboard/#
""" % {'name': name, 'link': secure_link}

    send_mail('Thanks for regstering, ' + name,
              msg, 'shapbasu@gmail.com', [email])
def addgame(request):
    if request.user.is_authenticated:
        player=Player.objects.get(user=request.user)
        if player.developer==True:# check before adding game if the user is developer or not
            form = AddGameForm(data=request.POST)
            if form.is_valid():
                gameDetails = form.save(commit=False)
                if not gameDetails.game_name.isalpha():#checking game name/id is alphabetic only
                    return render(request, "add_game.html", {"form": form, "msg": "Name should be alphabetic only without any spaces"})
                if Game.objects.filter(game_name=gameDetails.game_name).exists():#cehcking if game already exists
                    return render(request, "add_game.html", {"form": form, "msg": "ERROR: Name exists"})
                gameDetails.game_developer = request.user  # gets user
                gameDetails.save()
                return render(request, "add_game.html", {"form": form, "msg": "Game added successfully"})
            else:
                print(form.errors)
            return render(request, "add_game.html", {"form": form})
        else:
            return redirect("/dashboard")
    else:
        return redirect("/login")

def index(request):#redirects to dashboard page and fetches all games and send to index page.
    return render(request, 'index.html', {"allgames": Game.objects.all()})

def games(request):#redirects to dashboard page and fetches all games and send to index page.
    if request.user.is_authenticated:
        return render(request, 'games.html', {"allgames": Game.objects.all()})
    else:
        return redirect("/login")

def game(request, name):
    if request.user.is_authenticated:
        game = Game.objects.get(game_name=name)
        if Score.objects.filter(game=game, player=request.user).exists():
            return render(request, 'game.html', {"game": Game.objects.get(game_name=name.replace("_", " ")),"score":Score.objects.filter(game=game, player=request.user).exists()})
        else:
            return redirect('../begin_payment/' + name)
    else:
        return redirect('login')
def createPaymentID(username, game_name):
    pid = username
    pid += '____'
    pid += game_name
    return pid
"""
Calculating an MD5 checksum of the function arguement.
"""
def md5hex(tohash):

    try:
        import hashlib
        m = hashlib.md5()
    except:
        import md5
        m = md5.new()
    m.update(tohash)
    return m.hexdigest()

def begin_payment(request,game_name):
    if request.user.is_authenticated:
        game = Game.objects.get(game_name=game_name)
        pid = createPaymentID(request.user.username, game_name)  #just creating a payment by concact of username and game_name
        sid = "shaptarshibasu"
        price = game.game_price
        secret_key = "02994d1818b2e34a4ae79a0c00b9f474"
        checksum = 'pid={}&sid={}&amount={}&token={}'.format(pid, sid, price, secret_key)

        return render(request, 'begin_payment.html', {'game_name': game_name, 'pid': pid, 'price': price,
                                                  'checksum': md5hex(checksum.encode("ascii"))})
    else:
        return redirect("/login")
def payment_successful(request):
    """ The aim is to check whether player has already bought the game.If the player
        has not already paid then then redirect to payment or else throw appropriate error.
    """
    if request.user.is_authenticated:
        checksum = request.GET['checksum']
        ref = request.GET['ref']
        pid = request.GET['pid']
        result = request.GET['result']
        sid = "shaptarshibasu"
        secret_key = "02994d1818b2e34a4ae79a0c00b9f474"
        username, game_name = pid.split('____')
        game = Game.objects.get(game_name=game_name)
        checksum2 = 'pid={}&ref={}&result={}&token={}'.format(pid, ref, result, secret_key)
        print(md5hex(checksum.encode("ascii")))
        print()
        if md5hex(checksum2.encode("ascii")) == checksum:
            user = User.objects.get(username=username)
            if Score.objects.filter(game=game, player=user).exists():
                raise Http404("<h2> Payment need to be done only once. They game is already available for playing " + user.username)
            else:
                Score.objects.create(game=game, player=user, score=0)
                game.save()
            return render(request, 'payment_successful.html', {'game': game})
        else:
            return render(request, 'payment_failed.html')
    else:
        return redirect("/login")

def payment_failed(request):
    if request.user.is_authenticated:
        return render(request, 'payment_failed.html')
    else:
        return redirect("/login")
def payment_cancelled(request):
    if request.user.is_authenticated:
        return render(request, 'payment_cancelled.html')
    else:
        return redirect("/login")

def save(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.POST.get('state', None))
        state = data['gameState']
        states = json.dumps(state)
        game_name = request.POST.get('game_name', None)
        player_name = request.POST.get('player_name', None)
        game = Game.objects.get(game_name=game_name)
        user = User.objects.get(username=player_name)
        score = Score.objects.filter(game=game, player=user)
        score.update(state=states)
        return JsonResponse(states, safe=False)
    else:
        raise Http404('Not a post request check javascript')


def load(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.POST.get('json', None))
        game_name = request.POST.get('game_name', None)
        player_name = request.POST.get('player_name', None)
        game = Game.objects.get(game_name=game_name)
        user = User.objects.get(username=player_name)
        score = Score.objects.get(game=game, player=user)

        data["messageType"] = "LOAD"
        data["gameState"] = score.state
        if score.state:
            data["messageType"] = "LOAD"
            data["gameState"] = score.state

        return JsonResponse(data)
    else:
        raise Http404('Not a post request check javascript')
def score(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.POST.get('state', None))
        state = data['score']
        game_name = request.POST.get('game_name', None)
        player_name = request.POST.get('player_name', None)
        game = Game.objects.get(game_name=game_name)
        user = User.objects.get(username=player_name)
        score = Score.objects.filter(game=game, player=user)
        score.update(score=state)
        return JsonResponse(state, safe=False)
    else:
        raise Http404('Not a post request check javascript')

@api_view(['GET'])
def highscores(request, game_name):
    displayDetails=dict()
    if request.user.is_authenticated and not request.user.is_anonymous:
        gameDetails = Game.objects.get(game_name=game_name)
        scoresDetails = Score.objects.filter(game=gameDetails)
        if request.method == 'GET':
            details = {"game": gameDetails.game_name, "scores": {}}
            for score in scoresDetails:
                details["scores"][score.player.username] = score.score
                displayDetails[score.player.username]=score.score
            return render(request, 'displayHighScores.html', {'details':displayDetails})
    else:
        return redirect("/login")
