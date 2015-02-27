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

from flask import Blueprint, jsonify
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

mistune_available = True
try:
    import mistune
    from .ext.mistune_renderer import EmojiRenderer
except ImportError:
    mistune_available = False

bbcode_available = True
try:
    import bbcode
except ImportError:
    bbcode_available = False

supported_renderers = ["mistune", "bbcode", "standalone"]


def get_emojis():
    """Returns all emojis as a json object."""
    ctx = stack.top
    emoji = ctx.app.extensions["emoji"].emojis
    return jsonify(emoji)


def render_emoji(text):
    """Renders a text with emojis. Uses the configured renderer"""
    ctx = stack.top
    return ctx.app.extensions["emoji"].render(text)


def render_standalone(text):
    """Uses explicitly the standalone renderer."""
    ctx = stack.top
    return ctx.app.extensions["emoji"].render_standalone(text)


def render_mistune(text):
    """Uses explicitly the mistune renderer."""
    ctx = stack.top
    return ctx.app.extensions["emoji"].render_mistune(text)


def render_bbcode(text):
    """Uses explicitly the bbcode renderer."""
    ctx = stack.top
    return ctx.app.extensions["emoji"].render_bbcode(text)


class Emoji(object):
    """A extension to add Emoji support to your site.
    It also provides support for markdown via mistune
    and bbcode via bbcode but you have to use Flask-Emoji's renderer
    to use it. It should also be quite easy possible to implement support
    for other renderers. You can then add it with ``register_renderer()``.
    """

    def __init__(self, app=None):
        self.app = app
        # stores all the emojis
        self._emojis = dict()
        # the path to the static folder. defaults to the extensions
        # static folder
        self._static_path = pkg_resources.\
            resource_filename(__package__, "static")
        # the path to the emoji folder relative to the static folder.
        self._image_path = "emoji"
        # the full path to the emoji folder
        self._full_path = None
        # the static url path from where the emoji will be served.
        self._static_url_path = None
        # a dictionary containing all the renderers
        self._available_renderers = {"standalone": self.render_standalone}

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes the extension.

        :param app: The Flask application object
        """
        self.app = app
        # The path where the extension looks for emojis
        # Defaults to ``None``. If set to a path inside your static folder,
        # it will use this folder to look for emojis. The advantage about
        # the latter method is, that you can easily configure your webserver
        # to serve the emojis. Relative from your ``static`` directory.
        self.app.config.setdefault("EMOJI_IMAGE_PATH", None)

        # If you want to have a different static url for your emojis you
        # can define it here. Default is /static.
        # The full url is generated from the EMOJI_STATIC_URL + EMOJI_IMAGE_PATH
        self.app.config.setdefault("EMOJI_STATIC_URL", "/static")

        # The URL Prefix for the Blueprint. If ``None`` no one will be used.
        self.app.config.setdefault("EMOJI_URL_PREFIX", "/emoji")

        # The CSS class which should be used for emojis.
        self.app.config.setdefault("EMOJI_CSS_CLASS", "emoji")

        # Right now we support 2 different markup renderers.
        # bbcode and mistune. You'll also need to install them from PyPI.
        # Defaults to ``standalone``.
        self.app.config.setdefault("EMOJI_MARKUP_RENDERER", "standalone")

        # Ignored blocks. By default it will skip code blocks.
        self.app.config.setdefault("EMOJI_IGNORED_BLOCKS", ["codeblock"])

        # Now lets apply the config and register the blueprint
        self._configure_emoji()

        # Register the template filters
        self.app.jinja_env.filters["render_emoji"] = self.render

        # Register the Emoji state
        if not hasattr(self.app, "extensions"):
            self.app.extensions = {}
        self.app.extensions["emoji"] = self

        # Collect all available emojis
        self._emojis = self._collect_emojis()

    @property
    def emojis(self):
        """Returns all available Emojis."""
        return self._emojis

    def _configure_emoji(self):
        """Applies the configuration and registers the blueprint."""
        # Default full_path
        self._full_path = os.path.join(self._static_path, self._image_path)

        # Does the user want to use their own path?
        if self.app.config["EMOJI_IMAGE_PATH"] is not None:

            # if the path exists we use it otherwise we fallback to the
            # default ones
            if os.path.exists(os.path.join(
                    self.app.static_folder,
                    self.app.config["EMOJI_IMAGE_PATH"])):

                self._static_path = self.app.static_folder
                self._image_path = self.app.config["EMOJI_IMAGE_PATH"]
                self._full_path = os.path.join(self._static_path,
                                               self._image_path)

        self._static_url_path = "{}/{}".format(
            self.app.config["EMOJI_STATIC_URL"], self._image_path
        )
        bp = Blueprint("emoji", __name__, static_folder=self._full_path,
                       static_url_path=self._static_url_path)
        # If we would use the ``url_prefix`` it would also change the static url
        bp.add_url_rule("{}/all".format(self.app.config["EMOJI_URL_PREFIX"]),
                        view_func=get_emojis)
        self.app.register_blueprint(bp)

        # check which renderers are available and register them
        # Somehow I know that this can be done a lot nicer..
        if mistune_available:
            self.register_renderer("mistune", self.render_mistune)

        if bbcode_available:
            self.register_renderer("bbcode", self.render_bbcode)

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

    def register_renderer(self, name, renderer):
        """Registers a renderer.

        :param name: The name of the renderer
        :param renderer: The callback of the renderer
        """
        self._available_renderers[name] = renderer

    def image_string(self, name):
        """Returns the html version for a emoji.

        :param name: The name of the emoji.
        """
        src = "{}/{}".format(self._static_url_path, self._emojis[name])
        html = "<img class='{css}' alt='{alt}' src='{src}' />".format(
            css=self.app.config["EMOJI_CSS_CLASS"], alt=name, src=src
        )
        return html

    def render(self, text):
        """Renders the given text with one of the supported renderers.
        If the renderer is not available it will fall back to the standalone
        renderer.

        :param text: The text to be rendered.
        """
        return self._available_renderers.get(
            self.app.config["EMOJI_MARKUP_RENDERER"], "standalone"
        )(text)

    def render_standalone(self, text):
        """Renders the given text with emoji support.
        Possible HTML Entities are not escaped.

        :param text: The text which should be rendered.
        """
        pattern = re.compile(r':([a-z0-9\+\-_]+):', re.I)

        def emojify(match):
            value = match.group(1)

            if value in self._emojis:
                return self.image_string(value)
            return match.group(0)

        return pattern.sub(emojify, text)

    def render_mistune(self, text):
        """Renders the given text as markdown with emoji support.
        Falls back to the standalone renderer if the mistune library is not
        available.

        :param text: The text which should be rendered.
        """
        if not mistune_available:
            return self.render_standalone(text)

        renderer = EmojiRenderer(emojis=self._emojis,
                                 emoji_class=self.app.config["EMOJI_CSS_CLASS"],
                                 emoji_src=self._static_url_path)
        return mistune.Markdown(renderer=renderer)(text)

    def render_bbcode(self, text):
        """Renders the given text as bbcode with emoji support.
        Falls back to the standalone renderer if the bbcode library is not
        available.

        :param text: The text which should be rendered.
        """
        if not bbcode_available:
            return self.render_standalone(text)
