from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["client_id", "login", "age"]
    search_fields = ["client_id", "login", "age", "location", "gender"]
    list_filter = ["gender"]
