from django.contrib import admin
from .models import Clicknums, ClickDetail


@admin.register(Clicknums)
class Clicknums(admin.ModelAdmin):
    list_display = ('click_num', 'content_object')


@admin.register(ClickDetail)
class ClickDetail(admin.ModelAdmin):
    list_display = ('date', 'click_num', 'content_object')
