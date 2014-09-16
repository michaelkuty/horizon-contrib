import datetime

import django.forms

import horizon
from horizon import forms
from django.forms.extras.widgets import SelectDateWidget

class DateForm(forms.Form):
    """A simple form for selecting a range of time."""
    start = forms.DateField(input_formats=("%Y-%m-%d","%d.%m.%Y"))
    end = forms.DateField(input_formats=("%Y-%m-%d","%d.%m.%Y"))

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget.attrs['data-date-format'] = "dd-mm-yyyy"
        self.fields['end'].widget.attrs['data-date-format'] = "dd-mm-yyyy"