from django.contrib.auth.models import User
from django.db import models

class MacAddress(models.Model):
    user = models.ForeignKey(User)
    address = models.CharField(max_length=17)

    def __unicode__(self):
        return self.address
