from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Player, Team, Usage, XgLookup


class NoLoggingMixin:
    def log_addition(self, *args):
        return
    
    def log_change(self, *args):
        return

    def log_deletion(self, *args):
        return

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_delete_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
            obj.delete()

        return response

    export_as_csv.short_description = "Export Selected"
    export_delete_as_csv.short_description = "Export and Delete Selected"

@admin.register(Player)
class PlayerAdmin(NoLoggingMixin, admin.ModelAdmin, ExportCsvMixin):
    readonly_fields = ('updated',)
    actions = ['export_as_csv']

@admin.register(Team)
class TeamAdmin(NoLoggingMixin, admin.ModelAdmin, ExportCsvMixin):
    readonly_fields = ('updated',)
    actions = ['export_as_csv']

@admin.register(Usage)
class UsageAdmin(NoLoggingMixin, admin.ModelAdmin, ExportCsvMixin):
    readonly_fields = ('updated',)
    actions = ['export_as_csv', 'export_delete_as_csv']

@admin.register(XgLookup)
class XgLookupAdmin(NoLoggingMixin, admin.ModelAdmin, ExportCsvMixin):
    readonly_fields = ('updated',)
    actions = ['export_as_csv']