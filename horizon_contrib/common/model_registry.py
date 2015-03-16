
"""

This module supply django content type framework functions

We can register model class and get later.

``ModelRegistry`` is proxied to horizon singleton

.. code-block:: python

    import horizon

    horizon.model_registry.register(Foo)

    horizon.model_registry.get_model('foo')

TODO: iterate over INSTALLED_APPS and autoregister models

"""

import logging
import horizon

LOG = logging.getLogger(__name__)

MODELS = {}


class ModelRegistry(object):

    def register(self, model):

        global MODELS

        MODELS[model.__name__.lower()] = model

        return True

    def get_model(self, model_name):

        global MODELS

        name = model_name.lower()

        if name not in MODELS:
            raise Exception('Model %s not found in %s' % (name, MODELS))

        return MODELS[name]


model_registry = ModelRegistry()

horizon.model_registry = model_registry

# PROXIES


def register(model):

    model_registry.register(model)


def get_model(model_name):

    return model_registry.get_model(model_name)
