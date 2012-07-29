from django.template import Context, loader
from django.http import HttpResponse
from django.core import serializers
from garbagecollector.models import User
from network.network import network

def index(request):
    template = loader.get_template('garbagecollector/index.html')
    return HttpResponse(template.render(Context()))

def get_online(request):
    mac_addresses = network().get_online_mac_addesses()

    users = User.objects.filter(macaddress__address__in = mac_addresses);
    data = serializers.serialize("json", users)

    return HttpResponse(data, mimetype='application/json')
