from cmstats.resources import Root
from pyramid.view import view_config


@view_config(context=Root, name="submit", renderer="string")
def submit(request):
    device_id = request.params.get('device_id', None)
    device_name = request.params.get('device_name', None)
    device_version = request.params.get('device_version', None)
    device_country = request.params.get('device_country', None)
    device_carrier_id = request.params.get('device_carrier_id', None)
