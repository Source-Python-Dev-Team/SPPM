from django.contrib import admin

from .models import ForumUser


@admin.register(ForumUser)
class ForumUserAdmin(admin.ModelAdmin):
    readonly_fields = (
        'username',
        'id',
    )
