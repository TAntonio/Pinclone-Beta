from django.contrib import admin
from .models import Pin, Tag, Comment, Like, PinBoard


class PinAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ("Book Details", {"fields": ["title"]}),
    # ]

    list_display = ("title", "image", "")

admin.site.register(Pin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PinBoard)

