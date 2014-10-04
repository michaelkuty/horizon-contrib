# -*- coding: UTF-8 -*-
import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from crispy_forms.bootstrap import Tab, Container, ContainerHolder, TabHolder
from crispy_forms.utils import render_field, flatatt, TEMPLATE_PACK
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string


class ModelFormTab(Tab):

    """
    Tab object. It wraps fields in a div whose default class is "tab-pane" and
    takes a name as first argument. Example::

        Tab('tab_name', 'form_field_1', 'form_field_2', 'form_field_3')
    """
    css_class = 'tab-pane'
    link_template = '%s/layout/tab-link.html'

    template = "%s/layout/nemovitost_tab.html"

    def render_link(self, template_pack=TEMPLATE_PACK, **kwargs):
        """
        Render the link for the tab-pane. It must be called after render so css_class is updated
        with active if needed.
        """
        link_template = self.link_template % template_pack
        return render_to_string(link_template, {'link': self,
                                                "warn": u"Tento formulář neslouží pro editaci modelu !"})

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):

        if self.active:
            if not 'active' in self.css_class:
                self.css_class += ' active'
        else:
            self.css_class = self.css_class.replace('active', '')

        template = self.template % template_pack
        return render_to_string(template, {'div': self, 'form': self.model_form})

    def __init__(self, name, model_form, *fields, **kwargs):

        try:
            name = model_form.instance.__unicode__()
        except Exception, e:
            pass

        super(ModelFormTab, self).__init__(name, **kwargs)
        self.model_form = model_form


class TableTab(Tab):

    """
    Tab object. It wraps fields in a div whose default class is "tab-pane" and
    takes a name as first argument. Example::

        Tab('tab_name', 'form_field_1', 'form_field_2', 'form_field_3')
    """
    css_class = 'tab-pane'
    link_template = '%s/layout/tab-link.html'

    template = "%s/layout/table_tab.html"

    def render_link(self, template_pack=TEMPLATE_PACK, **kwargs):
        """
        Render the link for the tab-pane. It must be called after render so css_class is updated
        with active if needed.
        """
        link_template = self.link_template % template_pack
        return render_to_string(link_template, {'link': self
                                                })

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):

        if self.active:
            if not 'active' in self.css_class:
                self.css_class += ' active'
        else:
            self.css_class = self.css_class.replace('active', '')

        template = self.template % template_pack
        return render_to_string(template, {'div': self, 'table': self.table})

    def __init__(self, name, table, *fields, **kwargs):

        super(TableTab, self).__init__(name, **kwargs)

        self.table = table