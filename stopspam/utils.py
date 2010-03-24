from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


def akismet_check(request=None, comment_author='', comment_author_email='', comment_author_url='', comment_content='', akismet_api_key=None):
    """
    Connects to Akismet and returns True if Akismet marks this content as
    spam. Otherwise returns False.
    """

    # Check if the akismet library is installed
    try:
        from akismet import Akismet
    except ImportError:
        raise ImportError('Akismet library is not installed. "easy_install akismet" does the job.')

    # Check if the akismet api key is set, fail silently if
    # settings.DEBUG is False and return False (not moderated)
    AKISMET_API_KEY = akismet_api_key or getattr(settings, 'AKISMET_API_KEY', False)
    if not AKISMET_API_KEY:
        raise ImproperlyConfigured('You must set AKISMET_API_KEY with your api key in your settings file.')
    
    ak = Akismet(
        key = AKISMET_API_KEY,
        blog_url = 'http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
    )

    if ak.verify_key():
        if request is not None:
            data = {
                'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'referrer': request.META.get('HTTP_REFERER', ''),
            }
        else:
            data = {
                'user_ip': '',
                'user_agent': '',
                'referrer': '',
            }
        data.update({'comment_author': comment_author.encode('utf-8')})
        data.update({'comment_author_email': comment_author_email.encode('utf-8')})
        data.update({'comment_author_url': comment_author_url.encode('utf-8')})
        # Send the request to Akismet
        if ak.comment_check(comment_content.encode('utf-8'), data=data, build_data=True):
            return True
        
    return False