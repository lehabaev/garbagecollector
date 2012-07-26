from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class MacAddress(models.Model):
    user = models.ForeignKey(User)
    address = models.CharField(max_length=17)

    def __unicode__(self):
        return self.address
