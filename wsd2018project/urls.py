from django.urls import include, path
from django.contrib import admin
from django.conf.urls import url
import Play2Win.views
from django.contrib.auth import views as auth_views
from rest_framework import routers

urlpatterns = [
    url('dashboard/', Play2Win.views.index, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^register/$', Play2Win.views.UserFormView.as_view(),name='register'),
    url(r'^add_game/$', Play2Win.views.addgame, name='addgame'),
    url(r'^games/(\w+)$', Play2Win.views.game, name='game'),
    url(r'^games/$', Play2Win.views.games, name='games'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^begin_payment/(.+)$', Play2Win.views.begin_payment, name='begin_payment'),
    url(r'^payment_successful/.*', Play2Win.views.payment_successful),
    url(r'^payment_cancelled/.*', Play2Win.views.payment_cancelled),
    url(r'^payment_failed/.*', Play2Win.views.payment_failed),
    url(r'^save/', Play2Win.views.save),
    url(r'^load/', Play2Win.views.load),
    url(r'^score/', Play2Win.views.score),
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^highscores/(.+)$', Play2Win.views.highscores),
    path('admin/', admin.site.urls),

]
