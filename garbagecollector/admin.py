from django.contrib import admin
from garbagecollector.models import MacAddress

class MacAddressAdmin(admin.ModelAdmin):
  pass

admin.site.register(MacAddress, MacAddressAdmin)
