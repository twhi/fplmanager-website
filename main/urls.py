from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='home'),
    path('transfers/', views.transfers, name='transfers'),
    path('wildcard/', views.wildcard, name='wildcard'),
    path('lineup/', views.lineup, name='lineup'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout, name='logout'),
    path('ajax/get_autocomplete_players/', views.get_autocomplete_players, name='get_autocomplete_players'),
    path('ajax/receive_sim_form/', views.receive_sim_form, name='receive_sim_form'),
    path('ajax/login_creds/', views.login_creds_ajax, name='login_creds'),
    path('ajax/login_id/', views.login_id_ajax, name='login_id'),
    path('db_operations_211091', views.db_operations, name='db_operations'),
    path('refresh_team/', views.refresh_team, name='refresh_team'),
]