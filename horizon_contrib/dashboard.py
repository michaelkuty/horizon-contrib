

import horizon
from django.utils.translation import ugettext_lazy as _


class ContribDashboard(horizon.Dashboard):
    name = _("Horizon Contrib")
    slug = "contrib"
    panels = ('forms', 'generic')

    default_panel = 'forms'

    nav = False

    def get_absolute_url(self):
        # TODO: we haven't index
        # maybe search some model and returns his index
        return '/'


horizon.register(ContribDashboard)
