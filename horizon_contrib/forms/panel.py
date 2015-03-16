
import horizon
from django.utils.translation import ugettext_lazy as _
from horizon_contrib import dashboard


class FormsPanel(horizon.Panel):
    name = _("Forms")
    slug = 'forms'
    nav = False

dashboard.ContribDashboard.register(FormsPanel)
