from django.contrib import admin
from .models import Board, BoardFollower


class BoardAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Book Details", {"fields": ["title"]}),
    ]

    list_display = ("title",)

admin.site.register(Board)
admin.site.register(BoardFollower)

