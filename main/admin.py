from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, HttpResponse, redirect
from django import forms

import os
import csv
from io import TextIOWrapper, StringIO

from .models import Player, Team, Usage, XgLookup

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

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

class UploadCsvMixin:

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv)
        ]
        return my_urls + urls

    def import_csv(self, request):

        if request.method == 'POST':
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding=request.encoding)
            
            extension = os.path.splitext(request.FILES['csv_file'].name)[1]

            if extension == '.csv':
                reader = csv.reader(csv_file)
                
                headers = next(reader)

                model_fields = [m.name for m in self.model._meta.fields if m.name != 'updated']

                if set(headers) == set(model_fields):

                    input_data = [dict(zip(headers, row)) for row in reader]

                    for i in input_data:

                        t = self.model()

                        [setattr(t, k, v) for k, v in i.items()]

                        t.save()
                        
                else:
                    self.message_user(request, "Bad headers - unable to import selected file. Expected headers: '{expected}' Received headers: '{actual}'".format(
                        expected=model_fields,
                        actual=headers
                    ), level='ERROR')
                    return redirect("..")
            else:
                self.message_user(request, 'Incorrect file type', level='ERROR')
                return redirect('..')

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "custom_admin/csv_form.html", payload
        )



@admin.register(Player)
class PlayerAdmin(NoLoggingMixin, ExportCsvMixin, admin.ModelAdmin):
    readonly_fields = ('updated',)
    actions = ['export_as_csv']

@admin.register(Team)
class TeamAdmin(NoLoggingMixin, ExportCsvMixin, admin.ModelAdmin):
    readonly_fields = ('updated',)
    actions = ['export_as_csv']

@admin.register(Usage)
class UsageAdmin(NoLoggingMixin, ExportCsvMixin, admin.ModelAdmin):
    readonly_fields = ('updated',)
    actions = ['export_as_csv', 'export_delete_as_csv']

@admin.register(XgLookup)
class XgLookupAdmin(NoLoggingMixin, UploadCsvMixin, ExportCsvMixin, admin.ModelAdmin):
    change_list_template = 'custom_admin/models_changelist.html'
    readonly_fields = ('updated',)
    actions = ['export_as_csv']