from setuptools import setup, find_packages

setup(
    name='glamkit-stopspam',
    version='0.5.0',
    author='Julien Phalip',
    author_email='julien@interaction.net.au',
    description='A Django app to help you filter spam in your forms.',
    url='http://github.com/glamkit/glamkit-stopspam',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)