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
import pkg_resources

from flask import Blueprint, url_for, jsonify
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

mistune_available = True
try:
    import mistune
    from .ext.mistune_renderer import EmojiInlineLexer, EmojiRenderer
except ImportError:
    mistune_available = False

bbcode_available = True
try:
    import bbcode
except ImportError:
    bbcode_available = False


class EmojiError(Exception):
    """Error class if something went wrong here."""
    pass


def get_emojis():
    ctx = stack.top
    emoji = ctx.app.extensions["emoji"].emojis
    return jsonify(emoji)


class Emoji(object):
    """A extension to add Emoji support to your site."""

    def __init__(self, app=None):
        self._emojis = dict()
        self._static_path = pkg_resources.\
            resource_filename(__package__, "static")
        self._image_path = "emoji"
        self._full_path = None
        self._available_renderers = dict()

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

        # If you want to have a different static url for your emojis you
        # can define it here. Default is /static.
        # The full url is generated from the EMOJI_STATIC_URL + EMOJI_IMAGE_PATH
        app.config.setdefault("EMOJI_STATIC_URL", "/static")

        # The URL Prefix for the Blueprint. If ``None`` no one will be used.
        app.config.setdefault("EMOJI_URL_PREFIX", "/emoji")

        # The CSS class which should be used for emojis.
        app.config.setdefault("EMOJI_CSS_CLASS", "emoji")

        # Right now we support 2 different markup renderers.
        # bbcode and mistune. You'll also need to install them from PyPI.
        # Defaults to ``standalone``.
        app.config.setdefault("EMOJI_MARKUP_RENDERER", "standalone")

        # Ignored blocks. By default it will skip code blocks.
        app.config.setdefault("EMOJI_IGNORED_BLOCKS", ["codeblock"])

        # Now lets apply the config and register the blueprint
        self._configure_emoji(app)

        # Register the template filters
        app.jinja_env.filters["emoji"] = self.render_text

        # Register the Emoji state
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["emoji"] = self

        # Collect all available emojis
        self._emojis = self._collect_emojis()

    @property
    def emojis(self):
        """Returns all available Emojis."""
        return self._emojis

    @property
    def available_renderers(self):
        """Returns a dict with available renderers."""
        return

    def _configure_emoji(self, app):
        """Applies the configuration and registers the blueprint."""
        # Default full_path
        self._full_path = os.path.join(self._static_path, self._image_path)

        # Lets try to change it depending on the user configuration
        if app.config["EMOJI_IMAGE_PATH"] is not None:

            # if the path exists we use it otherwise we fallback to the
            # default ones
            if os.path.exists(os.path.join(app.static_folder,
                                           app.config["EMOJI_IMAGE_PATH"])):
                self._static_path = app.static_folder
                self._image_path = app.config["EMOJI_IMAGE_PATH"]
                self._full_path = os.path.join(self._static_path,
                                               self._image_path)

        static_url_path = "{}/{}".format(app.config["EMOJI_STATIC_URL"],
                                         self._image_path)
        bp = Blueprint("emoji", __name__, static_folder=self._full_path,
                       static_url_path=static_url_path)
        # If we would use the ``url_prefix`` it would also change the static url
        bp.add_url_rule("{}/all".format(app.config["EMOJI_URL_PREFIX"]),
                        view_func=get_emojis)
        app.register_blueprint(bp)

    def _collect_emojis(self):
        """Returns a dictionary containing all emojis with their
        name and filename. If the folder doesn't exist it returns a empty
        dictionary.
        """
        emojis = dict()

        # return an empty dictionary if the path doesn't exist
        if not os.path.exists(self._full_path):
            return emojis

        for emoji in os.listdir(self._full_path):
            emojis[emoji.split(".")[0]] = emoji

        return emojis

    def image_string(self, name):
        """Returns the html version for a emoji."""
        path = os.path.join(self._image_path, self._emojis[name])
        img = """<img class="{}" alt="{}" src="{}" />""".format(
            name, url_for("emoji.static", filename=path), "emoji"
        )

        return img

    def register_renderer(self, name, renderer):
        """TODO: Everything
        """
        self._available_renderers[name] = renderer

    def render_text(self, renderer, text):
        """TODO: Everything
        """
        return self.available_renderers[renderer](text)

    def render_standalone(self, text):
        """Renders the given text."""
        pattern = re.compile(r':([a-z0-9\+\-_]+):', re.I)

        def emojify(match):
            value = match.group(1)

            if value in self._emojis:
                return self.image_string(value)
            return match.group(0)

        return pattern.sub(emojify, text)

    def render_mistune(self, text):
        """Falls back to the standalone renderer if mistune is not available."""
        if not mistune_available:
            return self.render_standalone(text)

        renderer = EmojiRenderer()
        inline = EmojiInlineLexer(renderer=renderer,
                                  emojis=self.emojis,
                                  emoji_class="emoji",
                                  emoji_src=self._image_path)
        return mistune.Markdown(renderer=renderer, inline=inline)(text)

    def render_bbcode(self, text):
        pass


def render_emoji(text):
    pass
