from django import forms
from django.utils.translation import ugettext as _



# RECAPTCHA widgets
class RecaptchaResponse(forms.Widget):

    def render(self, *args, **kwargs):
        from recaptcha.client import captcha as recaptcha
        recaptcha_options = "<script> var RecaptchaOptions = { theme: 'clean' }; </script>\n"
        return recaptcha_options + recaptcha.displayhtml(self.public_key)

class RecaptchaChallenge(forms.Widget):
    is_hidden = True
    def render(self, *args, **kwargs):
        return ''
    
    
    
# Honeypot widget -- most automated spam posters will check any checkbox
# assuming it's an "I accept terms and conditions" box
class HoneypotWidget(forms.CheckboxInput):
    is_hidden = True
    def render(self, *args, **kwargs):
        wrapper_html = '<div style="display:none"><label for="id_accept">' + _('Are you a robot?') + '</label>%s</div>'
        return wrapper_html % super(HoneypotWidget, self).render(*args, **kwargs)