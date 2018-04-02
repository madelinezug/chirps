from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:announcement_id>/',views.detail,name='detail'),
    path('submit/',views.submit,name='submit')
]
