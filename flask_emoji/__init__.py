# -*- coding: utf-8 -*-
"""
    flask_emoji
    ~~~~~~~~~~~

    Flask-Emoji adds Emoji support to your site.

    :copyright: (c) 2015 by Peter Justin
    :license: BSD, see LICENSE for more details.
"""
import os
import re
from pkg_resources import resource_filename

import mistune
import emojipy

_re_emoji = re.compile(r'(?<!`)(:([\-\+a-z0-9_]+):)(?!`)', re.IGNORECASE)


class EmojiRenderer(object):
    def emoji(self, emoji):
        filename = "{}/{}".format("static", emoji)
        link = '<img class="{}" alt="{}" src="{}" />'.format(
            "emojione", emoji, filename
        )
        return link


class EmojiInlineLexer(mistune.InlineLexer):
    def __init__(self, **kwargs):
        super(EmojiInlineLexer, self).__init__(**kwargs)
        # add emoji rules
        self.rules.emoji = (emojipy.Emoji.unicode_compiled + emojipy.Emoji.ascii_compiled)
        self.default_rules.insert(0, 'emoji')

    def output_emoji(self, m):
        value = m.group(1)
        emoji = value.split(":")[1]
        return self.renderer.emoji(emoji)


class Emoji(object):
    """A extension to add Emoji support to your site."""

    def __init__(self, app=None):
        # the path to the static folder. defaults to the extensions
        # static folder
        self._static_path = resource_filename(__package__, "static")

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes the extension.

        :param app: The Flask application object
        """
        self.app = app

        # Register the Emoji state
        if not hasattr(self.app, "extensions"):
            self.app.extensions = {}
        self.app.extensions["emoji"] = self

    @property
    def emojis(self):
        """Returns all available Emojis."""
        pass

    def render(self, text):
        """Renders the given text with one of the supported renderers.
        If the renderer is not available it will fall back to the standalone
        renderer.

        :param text: The text to be rendered.
        """
        return self._available_renderers.get(
            self.app.config["EMOJI_MARKUP_RENDERER"], "standalone"
        )(text)

    def render_markdown(self, text):
        """Renders the given text as markdown with emoji support.
        Uses mistune as markdown renderer.

        :param text: The text which should be rendered.
        """
        renderer = EmojiRenderer(escape=True, hard_wrap=True)
        inline = EmojiInlineLexer(renderer=renderer)
        markdown = mistune.Markdown(renderer=renderer, inline=inline)
        return markdown(text)
