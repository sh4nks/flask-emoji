# -*- coding: utf-8 -*-
"""
    flask_emoji.ext.mistune.renderer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The Mistune renderer.

    :copyright: (c) 2015 by sh4nks
    :license: BSD, see LICENSE for more details.
"""

import re
from mistune import Renderer


class EmojiRenderer(Renderer):
    def __init__(self, **kwargs):
        self.emojis = kwargs.pop("emojis")
        self.emoji_class = kwargs.pop("emoji_class")
        self.emoji_src = kwargs.pop("emoji_src")

        super(EmojiRenderer, self).__init__(**kwargs)

    def paragraph(self, text):
        """Rendering paragraph tags. Like ``<p>`` with emoji support."""
        pattern = re.compile(r':([a-z0-9\+\-_]+):', re.I)

        def emojify(match):
            value = match.group(1)

            if value in self.emojis:
                filename = "{}/{}".format(self.emoji_src, self.emojis[value])
                link = '<img class="{}" alt="{}" src="{}" />'.format(
                    self.emoji_class, value, filename
                )
                return link
            return match.group(0)

        text = pattern.sub(emojify, text)
        return '<p>%s</p>\n' % text.strip(' ')
