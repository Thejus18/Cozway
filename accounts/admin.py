from django.contrib import admin
from django.contrib.auth.admin import UserAdmin         # for making the password Read only
from .models import Account


# Register your models here.
class AccountAdmin(UserAdmin):      # for making the password Read only
    list_display=('email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)             #-date_joined = Shows the descending order of the date joined

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account,AccountAdmin)
