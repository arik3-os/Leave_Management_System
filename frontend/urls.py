
from django import views
from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.Home, name='Home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]


