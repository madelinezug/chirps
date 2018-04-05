from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:announcement_id>/',views.detail,name='detail'),
    path('submit/',views.submit,name='submit'),
    path('sign_up/',views.sign_up,name='sign_up')
]
