# -*- coding: UTF-8 -*-
from django.conf import settings
from django.utils.html import format_html
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from horizon import tables
from horizon import tabs

# OBSOLETE

class AggregationMixin(tables.base.Column):
    """return html array of links for all models"""
    
    detail_url = "horizon:common:osoba:detail"
    
    field = None #must be M2M field
    
    #object mus have __unidoce__ and pk !!

    def get_raw_data(self, datum):
        output = []
        if self.field:
            objects = getattr(datum, self.field)
            for obj in objects.all():
                url = reverse(self.detail_url, args=[obj.pk,])
                link = u"<a href='%s'>%s</a>" % (url, obj)
                output.append(link)
        return format_html(', '.join(output))

class BaseAggregationMixin(object):
    """TODO impl table cell for field on same model
    """

class NestedAggregationMixin(object):
    """returns html table for django model with nested fields
    class Pohledavka(models.Model):

        test_field = models.ManyToManyField("Nested")

    class Nested(models.Model):

        test_field1 = Charfield etc..
        test_field2 = ..

    field = test_field
    nested_fields = ("test_field1", "test_field2")
    """
    thead = True
    field = None #must be M2M field
    _thead = None #readonly
    nested_fields = None
    _colspan = 0
    
    @property
    def colspan(self):
        try:
            self._colspan = len(list(self.nested_fields))
        except Exception, e:
            raise e
        return self._colspan
    
    @property
    def td_width(self):
        return 100 / self.colspan

    def get_thead(self, obj):
        thead = u"<thead><th colspan=\"{0}\">{1}</th></thead>"
        if not self.thead:
            return format_html(thead.format(0, ""))

        if len(self.nested_fields) > 0:
            tds = []
            for label in self.nested_fields:
                if label:
                    field_name = "field name"
                    try:
                        field_name = obj._meta.get_field_by_name(label)[0].name #name je vzdycky
                        field_name = obj._meta.get_field_by_name(label)[0].verbose_name
                    except Exception, e:
                        raise e
                    field_label = field_name.capitalize()
                    td = u"<td>{0}</td>".format(field_label)
                    tds.append(td)
            tr = u"<th>{0}</th>".format("".join(tds))
            thead = thead.format("".join(tr), self.colspan)
            return format_html(thead)
        return None

    def get_raw_data(self, datum):
        if self.field:
            objects = getattr(datum, self.field)
            trs = []

            if hasattr(objects, "all"): #django model support
                objects = objects.all()

            for obj in objects:
                if self._thead is None and obj:
                    self._thead = self.get_thead(obj)
                tds = []
                for field in self.nested_fields:
                    if field:
                        value = getattr(obj, field)
                        td = u"<td style=\"width:{0}%;\">{1}</td>".format(self.td_width, value)
                        tds.append(td)
                tr = u"<tr>{0}</tr>".format("".join(tds))
                trs.append(tr)
            table = u"<table style=\"width:100%;\">{0}{1}</table>".format(self._thead, "".join(trs))
            return format_html(table)
        return None
