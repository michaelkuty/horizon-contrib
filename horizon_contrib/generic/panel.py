
import horizon
from django.utils.translation import ugettext_lazy as _
from horizon_contrib import dashboard


class GenericPanel(horizon.Panel):
    name = _("Generic")
    slug = 'generic'
    nav = False

dashboard.ContribDashboard.register(GenericPanel)
