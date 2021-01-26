from django.contrib import admin

# Register your models here.
from users.models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id",)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id",)