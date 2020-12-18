from django import template

register = template.Library()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('tags')


@register.filter(name='get_tags_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.slug in request.GET.getlist('tags'):
        filters = new_request.getlist('tags')
        filters.remove(tag.slug)
        new_request.setlist('tags', filters)
    else:
        new_request.appendlist('tags', tag.slug)

    new_request.pop('page', None)

    return new_request.urlencode()
