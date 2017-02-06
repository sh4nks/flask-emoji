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
from setuptools import find_packages, setup

setup(
    name='Flask-Emoji',
    version='1.0.0',
    url='https://github.com/sh4nks/flask-emoji/',
    license='BSD',
    author='Peter Justin',
    author_email='peter.justin@outlook.com',
    description='Adds EmojiOne integration to your Flask application.',
    long_description=__doc__,
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.6',
        'mistune>=0.7.3',
        'emojipy>=0.1'
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
