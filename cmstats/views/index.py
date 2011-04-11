from cmstats.database.schema.devices import Device
from cmstats.resources import Root
from pyramid.view import view_config


@view_config(context=Root, renderer='index.mako')
def index(request):
    kwargs = {
            'device_count': Device.device_count(),
            'version_count': Device.version_count(),
            'total_nonkang': Device.count_nonkang(),
            'total_kang': Device.count_kang(),
    }

    return kwargs

@view_config(context=Root, name='test', renderer='derp.mako')
def test(request):
    return {}
