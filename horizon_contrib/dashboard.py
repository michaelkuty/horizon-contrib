

import horizon
from django.utils.translation import ugettext_lazy as _


class ContribDashboard(horizon.Dashboard):
    name = _("Horizon Contrib")
    slug = "contrib"
    panels = ('forms', 'generic')

    default_panel = 'forms'

    nav = False

horizon.register(ContribDashboard)
