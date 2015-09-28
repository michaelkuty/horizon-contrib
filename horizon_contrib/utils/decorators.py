



from functools import wraps

from django.conf import settings

GRAPHITE_ENDPOINT = getattr(settings, "GRAPHITE_ENDPOINT", None)


def graphite_context(view_func):
    """provide graphite endpoint to context
    """

    def inner(request, *args, **kwargs):
        context = view_func(request, *args, **kwargs)
        if isinstance(context, dict):
            context['graphite'] = GRAPHITE_ENDPOINT
        return context
    return wraps(view_func)(inner)
