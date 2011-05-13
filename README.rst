================
GLAMkit-stopspam
================

A tool for detecting and filtering spam in user input. It is part of the `GLAMkit project <http://glamkit.org/>`_. For more information, see the `documentation <http://docs.glamkit.org/documentation/stopspam/>`_.

View a full list of `GLAMkit components <http://docs.glamkit.org/components/>`_.

The approach
============

The stopspam app provides 3 forms of spam detection: Akismet, ReCAPTCHA, and a honeypot field. Each of those can be enabled in a given form by subclassing the form from the respective class. Note that since most of the below methods require access to the current request object, any forms that subclass the stopspam classes should be initalised in your views with the request as the first argument.

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

To use Akismet, an API key is also required (obtainable `on the Akismet website <http://akismet.com/>`_), which can either be provided as "AKISMET_API_KEY" in your Django settings file, or as an "akismet_api_key" property in your form. You also need to set your domain url in django admin "sites".

ReCAPTCHA
---------

ReCAPTCHA validation, enabled by subclassing RecaptchaForm, displays a CAPTCHA image in your form, requiring users to input two distorted words that appear in the image. The words are checked as part of the form validation, so a validation error will be thrown if the user fails to type in the words correctly.

An optional "recaptcha_always_validate" property can also be defined in the form, and will disable ReCAPTCHA validation if set to True, while still displaying the widget, which can come in handy during testing.

To use ReCAPTCHA, a pair of public and private API keys is required (obtainable `here <http://recaptcha.net/whyrecaptcha.html>`_), which can be provided either as "RECAPTCHA_PUBLIC_KEY" and "RECAPTCHA_PRIVATE_KEY" in you Django settings file, or as "recaptcha_public_key" and "recaptcha_private_key" properties in your form.

ReCAPTCHA comes with different themes ('clean', 'red', 'white', 'blackglass', 'custom'). You can choose a theme using "RECAPTCHA_THEME" in your Django settings file or by providing a "recaptcha_theme" property in your form. The default theme is 'clean'. If you choose 'custom' you have to provide some html in your template.

::

	<div id="recaptcha_widget" style="display:none">

		<div id="recaptcha_image"></div>
		<span class="recaptcha_only_if_incorrect_sol error_msg">{% trans "Incorrect please try again" %}</span>
		
		<label>
			<span class="recaptcha_only_if_image">{% trans "Enter the words above:" %}</span>
			<span class="recaptcha_only_if_audio">{% trans "Enter the numbers you hear:" %}</span>
		</label>
		
		<input type="text" id="recaptcha_response_field" name="recaptcha_response_field" />
		
		<div><a href="javascript:Recaptcha.reload()">{% trans "Get another CAPTCHA" %}</a></div>
		<div class="recaptcha_only_if_image">
			<a href="javascript:Recaptcha.switch_type('audio')">{% trans "Get an audio CAPTCHA" %}</a>
		</div>
		<div class="recaptcha_only_if_audio">
			<a href="javascript:Recaptcha.switch_type('image')">{% trans "Get an image CAPTCHA" %}</a>
		</div>
		
		<div><a href="javascript:Recaptcha.showhelp()">{% trans "Help" %}</a>
	
	</div>
	
	{{ form.recaptcha_response_field }}


Honeypot Field
--------------

Since most automated spam software will check any available checkboxes in a form, assuming they are "agree to terms and conditions" checkboxes, a honeypot field that must be left unchecked for the form to validate and is hidden from users using a "display:none" style can easily thwart most spam bots. The functionality is enabled by subclassing HoneyPotForm, and will throw a validation error if the checkbox is checked.

Dependencies:
=============

* Python libraries:
    - akismet (only if using `Akismet <http://akismet.com/>`_ checking)
    - recaptcha-client (only if using `ReCAPTCHA <http://recaptcha.net/>`_ validation)

* Accounts: an Akismet and/or ReCAPTCHA account is required to use the respective filtering functionality.
