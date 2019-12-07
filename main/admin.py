from django.contrib import admin
from .models import Player, Team

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)
