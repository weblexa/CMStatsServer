from pyramid.config import Configurator
from cmstats.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('cmstats.views.my_view',
                    context='cmstats:resources.Root',
                    renderer='cmstats:templates/mytemplate.pt')
    config.add_static_view('static', 'cmstats:static')
    return config.make_wsgi_app()

