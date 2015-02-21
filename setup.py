"""
Flask-Emoji
-----------

With Flask-Emoji it's super easy to add Emoji support to your site.


Installation
````````````

TODO


Resources
`````````

* `source <https://github.com/sh4nks/flask-emoji>`_
* `docs <https://flask-emoji.readthedocs.org/en/latest>`_
* `issues <https://github.com/sh4nks/flask-emoji/issues>`_

"""
from setuptools import setup

setup(
    name='Flask-Emoji',
    version='0.1',
    url='http://github.com/sh4nks/flask-emoji/',
    license='BSD',
    author='sh4nks',
    author_email='sh4nks7@gmail.com',
    description=
        'A extension to add Emoji support to your site.',
    long_description=__doc__,
    packages=['flask_emoji'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.6',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose>=1.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
