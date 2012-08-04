from django.contrib.auth.models import User
from django.template import Context, loader
from django.http import HttpResponse
import json
from garbagecollector.models import  MacAddress
from network.network import network

def index(request):
    template = loader.get_template('garbagecollector/index.html')
    return HttpResponse(template.render(Context()))

def get_online(request):
    mac_addresses = network().get_online_mac_addesses()
    online_users = MacAddress.objects.filter(address__in = mac_addresses).distinct()
    online_ids = online_users.values_list('id', flat=True)
    offline_users = User.objects.exclude(id__in = online_ids)

    data = {
        'online': map(lambda x: {'first_name': x.first_name, 'last_name': x.last_name}, online_users),
        'offline': map(lambda x: {'first_name': x.first_name, 'last_name': x.last_name}, offline_users)
    }

    return HttpResponse(json.dumps(data), mimetype='application/json')
