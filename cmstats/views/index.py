from cmstats.database.schema.devices import Device
from cmstats.resources import Root
from pyramid.view import view_config


@view_config(context=Root, renderer="index.mako")
def index(request):
    total_devices = Device.count()
    return {'total_devices': total_devices}
