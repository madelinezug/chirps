from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:announcement_id>/', views.detail, name='detail'),
    path('individuals/<str:individual_email>/', views.individual_detail, name='individual_detail'),
    path('submit/', views.submit, name='submit'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('saved/', views.saved, name='saved'),
    path('my_chirps/', views.my_chirps, name='my_chirps'),
    path('individuals/', views.individuals, name='individuals'),
    path('email_digest/', views.email_digest, name='email_digest'),
    path('pending/', views.pending, name='pending'),
    path('search/<str:search_key>', views.search, name='search_tags'),
    path('edit/<int:announcement_id>/', views.edit, name='edit'),
    path('reset_pw/', views.reset_pw, name='reset_pw')
]
