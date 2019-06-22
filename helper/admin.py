from django.contrib import admin

from helper.models import UserData


class UserDataAdmin(admin.ModelAdmin):
    list_display = ['id']
    search_fields = ['id']


admin.site.register(UserData, UserDataAdmin)
