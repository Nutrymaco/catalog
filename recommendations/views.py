from pyramid.renderers import render_to_response, get_renderer
import pyramid_jinja2


def recommendations(request):
    if request.method == 'GET':
        ...
