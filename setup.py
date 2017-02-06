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
import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTestCommand(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


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
    test_suite='tests',
    tests_require=[
        'py',
        'pytest',
        'pytest-cov'
    ],
    cmdclass={'test': PyTestCommand},
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
