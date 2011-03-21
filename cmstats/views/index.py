from cmstats.database.schema.devices import Device
from cmstats.resources import Root
from pyramid.view import view_config


@view_config(context=Root, renderer="index.mako")
def index(request):
    device_count = Device.device_count()
    total_devices = Device.count()
    return {
            'total_devices': total_devices,
            'device_count': device_count
    }
