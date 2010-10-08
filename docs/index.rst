Stopspam
========

The stopspam app provides three forms of spam detection: Akismet, ReCAPTCHA, and a honeypot field. Each of those can be enabled in a given form by subclassing the form from the respective class. Note that since most of the below methods require access to the current request object, any forms that subclass the stopspam classes should be initalised in your views with the request as the first argument.

.. rubric:: This is part of the GLAMkit Project. For more information, please visit http://glamkit.org.

Akismet
-------

Akismet filtering, enabled by subclassing AkismetForm, sends off user input to the Akismet servers to determine whether it is likely to be spam. The request must be explicitly invoked using the akismet_check() method, allowing you to determine how to handle spam messages (e.g. if archiving such messages is desired).

Akismet filtering also requires an "akismet_fields" dictionary to be defined as a property of your form, mapping the fields in the form to Akismet fields as shown below. Note that only the "comment_content" item is strictly required.

::

	class YourForm(AkismetForm):
		akismet_fields = {
				'comment_author': 'name',
				'comment_author_email': 'email',
				'comment_author_url': 'url',
				'comment_content': 'comment',
				}
		name = forms.CharField(...)
		url = forms.URLField(...)
		email = forms.EmailField(...)
		comment = forms.TextField(...)

To use Akismet, an API key is also required (obtainable `on the Akismet website <http://akismet.com/>`_), which can either be provided as "AKISMET_API_KEY" in your Django settings file, or as an "akismet_api_key" property in your form.

ReCAPTCHA
---------

ReCAPTCHA validation, enabled by subclassing RecaptchaForm, displays a CAPTCHA image in your form, requiring users to input two distorted words that appear in the image. The words are checked as part of the form validation, so a validation error will be thrown if the user fails to type in the words correctly.

An optional "recaptcha_always_validate" property can also be defined in the form, and will disable ReCAPTCHA validation if set to True, while still displaying the widget, which can come in handy during testing.

To use ReCAPTCHA, a pair of public and private API keys is required (obtainable `here <http://recaptcha.net/whyrecaptcha.html>`_), which can be provided either as "RECAPTCHA_PUBLIC_KEY" and "RECAPTCHA_PRIVATE_KEY" in your Django settings file, or as "recaptcha_public_key" and "recaptcha_private_key" properties in your form.

Honeypot Field
--------------

Since most automated spam software will check any available checkboxes in a form, assuming they are "agree to terms and conditions" checkboxes, a honeypot field that must be left unchecked for the form to validate and is hidden from users using a "display:none" style can easily thwart most spam bits. The functionality is enabled by subclassing HoneyPotForm, and will throw a validation error if the checkbox is checked.

Dependencies:
=============
* Accounts: an Akismet and/or ReCAPTCHA account is required to use the respective filtering functionality.
* Python libraries:
    - akismet (only if using `Akismet <http://akismet.com/>`_ checking)
    - recaptcha-client (only if using `ReCAPTCHA <http://recaptcha.net/>`_ validation)

