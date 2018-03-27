from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:announcement_id>/',views.atext,name='description'),
]
