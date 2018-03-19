from django.urls import include, path
from django.contrib import admin
from django.conf.urls import url
import Play2Win.views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url('dashboard/', Play2Win.views.index, name='index'),
    path('admin/', admin.site.urls),
]
