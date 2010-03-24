from django import forms
from django.core.exceptions import ValidationError

from widgets import HoneypotWidget


class HoneypotField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        super(HoneypotField, self).__init__(
              widget = HoneypotWidget,
              required = False,
              error_messages = { 'checked': 'Please don\'t check this box.' },
              *args, **kwargs)
    
    def clean(self, value):
        val = super(HoneypotField, self).clean(value)
        if val:
            raise ValidationError(self.error_messages['checked'])
        return val