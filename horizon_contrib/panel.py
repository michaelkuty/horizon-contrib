
import logging

import horizon
from django.core.urlresolvers import reverse

LOG = logging.getLogger(__name__)


class ModelPanel(horizon.Panel):

    url = 'horizon:contrib:generic:index'

    def get_absolute_url(self):
        """Returns the default URL for this panel.
        The default URL is defined as the URL pattern with ``name="index"`` in
        the URLconf for this panel.
        """
        try:
            if hasattr(self, 'model_class'):
                args = [self.model_class]

                if hasattr(self, 'react'):
                    args += ['react']

                return reverse(self.url, args=args)

            return reverse('horizon:%s:%s:%s' % (self._registered_with.slug,
                                                 self.slug,
                                                 self.index_url_name))
        except Exception as exc:
            # Logging here since this will often be called in a template
            # where the exception would be hidden.
            LOG.info("Error reversing absolute URL for %s: %s" % (self, exc))
            raise
