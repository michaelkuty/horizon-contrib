

from django.utils.translation import ugettext_lazy as _

import horizon


class ContribDashboard(horizon.Dashboard):
    name = _("Horizon Contrib")
    slug = "contrib"

    panels = ('forms', 'generic')

    default_panel = 'forms'

horizon.register(ContribDashboard)
