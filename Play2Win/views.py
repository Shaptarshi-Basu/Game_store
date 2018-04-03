from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from .forms import UserForm
from .models import *


class UserFormView(View):
    form_class = UserForm
    template='templates/registration.html'

    #display blank form
    def get(self,request):
        form = UserForm()  # 3ICE: Possibly stop using this, since we need to send the email
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
            dev = request.POST.get("developer", "not_developer") == "developer_box"  # check if developer
            user_db.developer = dev
            user_db.save()
            player = Player.objects.create(user=user_db, developer=dev, activated=False)
            hashed_password = user_db.password
            send_confirmation_mail(name, hashed_password, email)
            # if dev in ["developer_box"]: #3ICE: This is not how you check the existence of a checkbox.
            #    return redirect('registration')
            # else:
            #    return redirect('profile_player')
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

    # <a href="https://daak-store.herokuapp.com/user_verification/""" + secure_link + """
    # ">https://daak-store.herokuapp.com/user_verification/""" + secure_link + """</a>
    send_mail('Please confirm your registration, ' + name,
              msg, 'shapbasu@gmail.com', [email])


def index(request):
    return render(request, 'index.html')
