from django.urls import path

from . import views

app_name = 'psite'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.generate, name='generate'),
    # path('poetry', views.poetry, name='poetry'),
]