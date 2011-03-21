from pyramid.config import Configurator
from cmstats.resources import Root

def main(global_config, **settings):
    config = Configurator(root_factory=Root, settings=settings)
    config.scan('cmstats.views')

    return config.make_wsgi_app()

