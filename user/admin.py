from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, OAuthRelationship


@admin.register(OAuthRelationship)
class OAuthRelationship(admin.ModelAdmin):
    list_display = ('user', 'oauth_type', 'node_id')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'nickname', 'email', 'is_staff', 'is_active', 'is_superuser')

    def nickname(self, obj):
        return obj.profile.nickname

    nickname.short_description = '昵称'


# Re_register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Register your models here
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')
