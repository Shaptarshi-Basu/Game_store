from django.urls import include, path
from django.contrib import admin
from django.conf.urls import url
import Play2Win.views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url('dashboard/', Play2Win.views.index, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^register/$', Play2Win.views.UserFormView.as_view(),name='register'),
    url(r'^add_game/$', Play2Win.views.addgame, name='addgame'),
    url(r'^games/(\w+)$', Play2Win.views.game, name='game'),
    url(r'^games/$', Play2Win.views.games, name='games'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
]
