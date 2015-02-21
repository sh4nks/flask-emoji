# -*- coding: utf-8 -*-
"""
    flask_emoji
    ~~~~~~~~~~~

    Flask-Emoji adds Emoji support to your site.

    :copyright: (c) 2015 by sh4nks
    :license: BSD, see LICENSE for more details.
"""


class Emoji(object):
    """Emoji"""

    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes the extension.

        :param app: The Flask application object
        """
        # Register the template filters
        app.jinja_env.filters["emoji"] = render_emoji

        # Register the Emoji state
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["emoji"] = self

    def get_by_category(self, category):
        """Returns all Emojis from a category.

        :param category: The name of the category.
                         Available categories are: people, nature, objects,
                         places, symbols
        """
        pass

    def get_all():
        """Returns all available Emojis."""
        pass


def render_emoji(text):
    """Renders the Emojis in the given text.

    :param text: The text to be rendered.
    """
    pass
