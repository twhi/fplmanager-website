from django.contrib import admin
from .models import Player, Team, Usage

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)
