from django.contrib import admin
from .models import Player, Team, Usage

class NoLoggingMixin:
    def log_addition(self, *args):
        return
    
    def log_change(self, *args):
        return

    def log_deletion(self, *args):
        return

@admin.register(Player)
class PlayerAdmin(NoLoggingMixin, admin.ModelAdmin):
    readonly_fields = ('updated',)

@admin.register(Team)
class TeamAdmin(NoLoggingMixin, admin.ModelAdmin):
    readonly_fields = ('updated',)

@admin.register(Usage)
class UsageAdmin(NoLoggingMixin, admin.ModelAdmin):
    readonly_fields = ('updated',)
