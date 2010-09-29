from django import forms
from django.utils.translation import ugettext as _, get_language
from django.utils.safestring import mark_safe


# RECAPTCHA widgets
class RecaptchaResponse(forms.Widget):

    def render(self, *args, **kwargs):
        from recaptcha.client import captcha as recaptcha
        recaptcha_options = "<script> var RecaptchaOptions = { theme: '" + self.theme + \
                            "', lang: '" + get_language()[0:2] + \
                            ("', custom_theme_widget: 'recaptcha_widget'" if self.theme == 'custom' else "'") + " }; </script>\n"
        return mark_safe(recaptcha_options + recaptcha.displayhtml(self.public_key))


class RecaptchaChallenge(forms.Widget):
    is_hidden = True
    def render(self, *args, **kwargs):
        return ""
#        return mark_safe('')
    
    
    
# Honeypot widget -- most automated spam posters will check any checkbox
# assuming it's an "I accept terms and conditions" box
class HoneypotWidget(forms.CheckboxInput):
    is_hidden = True
    def render(self, *args, **kwargs):
        wrapper_html = '<div style="display:none"><label for="id_accept_terms">' + _('Are you a robot?') + '</label>%s</div>'
        return mark_safe(wrapper_html % super(HoneypotWidget, self).render(*args, **kwargs))