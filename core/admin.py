from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html

from .models import *

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = "Профиль"
    verbose_name_plural = "Профили"
    fk_name = "user"
    max_num = 1

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "profile_name",)
    list_select_related = ("profile",)
    search_fields = ("username", "email", "profile__name")
    list_filter = ("username", "email", "profile__name")

    @admin.display(description="Имя в профиле")
    def profile_name(self, obj):
        return getattr(obj.profile, "name", "-")


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "avatar_url")
    search_fields = ("name", "user__username", "user__email")
    list_select_related = ("user",)
    list_filter = ("name", "user__username", "user__email")
    raw_id_fields = ("user",)
    ordering = ("pk",)