from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from .forms import UserForm,AddGameForm
from .models import *


class UserFormView(View):
    form_class = UserForm
    template='templates/registration.html'

    #display blank form
    def get(self,request):
        form = UserForm()
        return render(request, 'registration.html', {'form': form})
    #process form data
    def post(self,request):
        form = UserForm(request.POST)
        if form.is_valid():
            user_db = form.save(commit=False)
            name = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            if not name.isalpha():
                return render(request, 'registration.html', {'form': form, 'msg':"Use only alpha numeric"})
            user = authenticate(username=name, password=raw_password)
            dev = request.POST.get("developer", "not_developer") == "developer_box"  # check if its a developer or player
            user_db.developer = dev
            user_db.save()
            player = Player.objects.create(user=user_db, developer=dev, activated=False)
            hashed_password = user_db.password
            send_confirmation_mail(name, hashed_password, email)
            return redirect('login')
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
def send_confirmation_mail(name, pw, email):
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
        form = AddGameForm(data=request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            if not game.game_name.isalpha():
                return render(request, "add_game.html", {"form": form, "msg": "Please specify an alphanumeric game name (It's the Game ID)"})
            if Game.objects.filter(game_name=game.game_name).exists():
                return render(request, "add_game.html", {"form": form, "msg": "ERROR: That name is already in use"})
            game.game_developer = request.user  # gets user
            game.save()
            return render(request, "add_game.html", {"form": form, "msg": "Game added successfully"})
        else:
            print(form.errors)
        return render(request, "add_game.html", {"form": form})
    else:
        return redirect("/login")

def index(request):
    return render(request, 'index.html', {"allgames": Game.objects.all()})
def game(request, name):
    if request.user.is_authenticated:
        game = Game.objects.get(game_name=name)
        if Score.objects.filter(game=game, player=request.user).exists():
            return render(request, 'game.html', {"game": Game.objects.get(game_name=name.replace("_", " "))})
        else:
            return redirect('../begin_payment/' + name)
    else:
        return redirect('login')
def games(request):
    if request.user.is_authenticated:
        return render(request, 'games.html', {"allgames": Game.objects.all()})
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
    # create a logic which takes care of checking whether player has already bought the game
    # if the player has already purchased, throw error, navigate back to the game
    # else add player to the game or vice versa, navigate back to the games list
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
                raise Http404("<h2> You don't have to pay us twice!,You already have the game in your inventory " + user.username)
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
