from django.contrib import admin
from garbagecollector.models import User, MacAddress

class MacAddressInline(admin.StackedInline):
    model = MacAddress
    extra = 1

class UserAdmin(admin.ModelAdmin):
    inlines = [MacAddressInline]

admin.site.register(User, UserAdmin)
