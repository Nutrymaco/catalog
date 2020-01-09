from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from items.views import *
from recommendations.views import *
from users.views import *
from shops.views import *
from offers.views import *


def main():
    api_prefix = 'api/v1/'
    with Configurator() as config:
        config.add_route('items', api_prefix + 'items')
        config.add_view(items, route_name='items')
        config.add_route('item', api_prefix + 'items/{item_id}')
        config.add_view(item, route_name='item')

        config.add_route('shops', api_prefix + 'shops')
        config.add_view(shops, route_name='shops')
        config.add_route('shop', api_prefix + 'shops/{shop_id}')
        config.add_view(shop, route_name='shop')

        config.add_route('offers', api_prefix + 'offers')
        config.add_view(offers, route_name='offers')
        config.add_route('offer', api_prefix + 'offers/{shop_offer_id}')
        config.add_view(offer, route_name='offer')

        config.add_route('users', api_prefix + 'users')
        config.add_view(users, route_name='users')
        config.add_route('user', api_prefix + 'users/{user_id}')
        config.add_view(user, route_name='user')

        config.add_route('recommendations', api_prefix + 'recommendations')
        config.add_view(recommendations, route_name='recommendations')

        config.include('pyramid_jinja2')
        application = config.make_wsgi_app()

    server = make_server('0.0.0.0', 8000, app=application)
    server.serve_forever()


if __name__ == "__main__":
    main()
