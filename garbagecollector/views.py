from django.template import Context, loader
from django.http import HttpResponse
from network.network import network

def index(request):
    template = loader.get_template('garbagecollector/index.html')
    return HttpResponse(template.render(Context()))

def test(request):
    mac = network().get_online_mac_addesses()
    return HttpResponse('<br />'.join(mac))
