# -*- coding: utf-8 -*-
"""
    flask_emoji
    ~~~~~~~~~~~

    Flask-Emoji adds Emoji support to your site.

    :copyright: (c) 2015 by sh4nks
    :license: BSD, see LICENSE for more details.
"""
import os
import re
from flask import Blueprint, url_for
import pkg_resources
markdown_available = True
try:
    import markdown
except ImportError:
    markdown_available = False

bbcode_available = True
try:
    import bbcode
except ImportError:
    bbcode_available = False


class Emoji(object):
    """A extension to add Emoji support to your site. I"""

    def __init__(self, app=None):
        self.app = app
        self._emojis = dict()
        self._static_path = pkg_resources.\
            resource_filename(__package__, "static")
        self._image_path = "emoji"

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes the extension.

        :param app: The Flask application object
        """
        # The path where the extension looks for emojis
        # Defaults to ``None``. If set to a path inside your static folder,
        # it will use this folder to look for emojis. The advantage about
        # the latter method is, that you can easily configure your webserver
        # to serve the emojis. Relative from your ``static`` directory.
        app.config.setdefault("EMOJI_IMAGE_PATH", None)

        # The URL Prefix for the Blueprint. If ``None`` no one will be used.
        app.config.setdefault("EMOJI_URL_PREFIX", None)

        # The CSS class which should be used for emojis.
        app.config.setdefault("EMOJI_CSS_CLASS", "emoji")

        # Right now we support 2 different markup renderers.
        # bbcode and markdown2. If left blank, it will use it's own.
        app.config.setdefault("EMOJI_MARKUP_RENDERER", None)

        # Ignored blocks. By default it will skip code blocks.
        app.config.setdefault("EMOJI_IGNORED_BLOCKS", ["codeblock"])

        if app.config["EMOJI_IMAGE_PATH"] is not None:
            # if the path exists, we use it otherwise we fallback to ours
            if os.path.exists(app.root_path, app.config["EMOJI_IMAGE_PATH"]):
                self._static_path = app.static_folder
                self._image_path = app.config["EMOJI_IMAGE_PATH"]

        # Doesn't work as expected yet.
        blueprint = Blueprint("emoji", __name__,
                              static_folder=app.config["EMOJI_IMAGE_PATH"])
        app.register_blueprint(blueprint,
                               url_prefix=app.config["EMOJI_URL_PREFIX"])

        # Register the template filters
        app.jinja_env.filters["emoji"] = self.render_text

        # Register the Emoji state
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["emoji"] = self

        # Collect all available emojis
        self._emojis = self._collect_emojis()

    def _collect_emojis(self):
        """Returns a dictionary containing all emojis with their
        corresponding name.
        """
        emojis = dict()
        path = os.path.join(self._static_path, self._image_path)
        for emoji in os.listdir(path):
            emojis[emoji.split(".")[0]] = emoji

        return emojis

    def get_all(self):
        """Returns all available Emojis."""
        return self._emojis

    def image_string(self, name):
        """Renders a emoji."""
        path = os.path.join(self._image_path, self._emojis[name])
        out = """<img class="{}" alt="{}" src="{}" />""".format(
            name, url_for("static", filename=path), "emoji"
        )

        return out

    def render_text(self, text):
        """Renders the given text."""
        pattern = re.compile(r':([a-z0-9\+\-_]+):', re.I)

        def emojify(match):
            value = match.group(1)

            if value in self._emojis:
                return self.image_string(value)
            return match.group(0)

        return pattern.sub(emojify, text)
