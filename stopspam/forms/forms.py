from django import forms
from django.conf import settings

from stopspam import utils

from fields import HoneypotField
from widgets import RecaptchaChallenge, RecaptchaResponse
from django.utils.translation import ugettext as _



class BaseForm(forms.Form):
    
    def __init__(self, request, *args, **kwargs):
        self._request = request
        super(BaseForm, self).__init__(*args, **kwargs)
        



class AkismetForm(BaseForm):
    
    akismet_fields = {
            'comment_author': 'name',
            'comment_author_email': 'email',
            'comment_author_url': 'url',
            'comment_content': 'comment',
            }
    akismet_api_key = None
    
    def akismet_check(self):
        fields = {}
        for key, value in self.akismet_fields.items():
            fields[key] = self.cleaned_data[value]
        return utils.akismet_check(self._request, akismet_api_key=self.akismet_api_key, **fields)


class RecaptchaForm(BaseForm):
    recaptcha_challenge_field = forms.CharField(widget=RecaptchaChallenge)
    recaptcha_response_field = forms.CharField(
                widget = RecaptchaResponse,
                label = _('Please enter the two words on the image separated by a space:'),
                error_messages = {
                    'required': _('You did not enter any of the words.')
            })
    recaptcha_always_validate = False
    
    def __init__(self, *args, **kwargs):
        super(RecaptchaForm, self).__init__(*args, **kwargs)
        self._recaptcha_public_key = getattr(self, 'recaptcha_public_key', getattr(settings, 'RECAPTCHA_PUBLIC_KEY'))
        self._recaptcha_private_key = getattr(self, 'recaptcha_private_key', getattr(settings, 'RECAPTCHA_PRIVATE_KEY'))
        self.fields['recaptcha_response_field'].widget.public_key = self._recaptcha_public_key
        
    def clean_recaptcha_response_field(self):
        if 'recaptcha_challenge_field' in self.cleaned_data:
            self._validate_captcha()
        return self.cleaned_data['recaptcha_response_field']

    def clean_recaptcha_challenge_field(self):
        if 'recaptcha_response_field' in self.cleaned_data:
            self._validate_captcha()
        return self.cleaned_data['recaptcha_challenge_field']
    
    def _validate_captcha(self):
        if not self.recaptcha_always_validate:
            rcf = self.cleaned_data['recaptcha_challenge_field']
            rrf = self.cleaned_data['recaptcha_response_field']
            if rrf == '':
                raise forms.ValidationError(_('You did not enter the two words shown in the image.'))
            else:
                from recaptcha.client import captcha as recaptcha
                ip = self._request.META['REMOTE_ADDR']
                check = recaptcha.submit(rcf, rrf, self._recaptcha_private_key, ip)
                if not check.is_valid:
                    raise forms.ValidationError(_('The words you entered did not match the image'))

class HoneyPotForm(BaseForm):
    accept_terms = HoneypotField()
    


class SuperSpamKillerForm(RecaptchaForm, HoneyPotForm, AkismetForm):
    pass