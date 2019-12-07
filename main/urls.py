from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='home'),
    path('transfers/', views.transfers, name='transfers'),
    path('wildcard/', views.wildcard, name='wildcard'),
    path('lineup/', views.lineup, name='lineup'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('ajax/get_players/', views.get_players, name='get_players'),
    path('ajax/receive_form/', views.receive_form, name='receive_form'),
    path('db_operations_211091', views.db_operations, name='db_operations')
]