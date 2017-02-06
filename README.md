[![Build Status](https://travis-ci.org/sh4nks/flask-emoji.svg?branch=master)](https://travis-ci.org/sh4nks/flask-emoji)
[![Coverage Status](https://coveralls.io/repos/sh4nks/flask-emoji/badge.png)](https://coveralls.io/r/sh4nks/flask-emoji)

# Flask-Emoji

Flask-Emoji provides an easy way to add emoji support to your Flask
application.


# Quickstart

Install it from PyPI:

    $ pip install Flask-Emoji

You can either bind Flask-Emoji directly to a specific application instance

    app = Flask(__name__)
    emoji = Emoji(app)

or by using the factory pattern, you can bind it to one or more instances:

    emoji = Emoji()
    def create_app():
        app = Flask(__name__)
        emoji.init_app(app)
        return app


# Links

* [Documentation](https://flask-emoji.readthedocs.io)
* [Source Code](https://github.com/sh4nks/flask-emoji)
* [Issues](https://github.com/sh4nks/flask-emoji/issues)
