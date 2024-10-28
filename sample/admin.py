from django.contrib import admin
from .models import TestContentMaker


@admin.register(TestContentMaker)
class TestContentMakerAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'subscribers', 'played')


