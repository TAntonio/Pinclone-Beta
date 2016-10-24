from django.contrib import admin
from .models import Pin, Tag


class PinAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ("Book Details", {"fields": ["title"]}),
    # ]

    list_display = ("title", "image", "")

admin.site.register(Pin)
admin.site.register(Tag)
