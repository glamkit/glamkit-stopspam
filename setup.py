from setuptools import setup, find_packages

setup(
    name='glamkit-stopspam',
    version='0.0.1',
    description='A Django app to help you remove spam from your menu.',
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