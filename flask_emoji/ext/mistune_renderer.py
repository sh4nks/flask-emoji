import copy
import re
from mistune import Renderer, InlineGrammar, InlineLexer


class EmojiRenderer(Renderer):
    def emoji(self, emoji_class, emoji_alt, emoji_src):
        return '<img class="{}" alt="{}" src="{}" />'.format(
            emoji_class, emoji_src, emoji_alt
        )


class EmojiInlineGrammar(InlineGrammar):
    # it would take a while for creating the right regex
    emoji = re.compile(r':([a-z0-9\+\-_]+):', re.I)


class EmojiInlineLexer(InlineLexer):
    default_rules = copy.copy(InlineLexer.default_rules)

    # Add emoji parser to default rules
    # you can insert it any place you like
    default_rules.insert(3, 'emoji')

    def __init__(self, renderer, rules=None, **kwargs):
        if rules is None:
            # use the inline grammar
            rules = EmojiInlineGrammar()

        self.emojis = kwargs.pop("emojis")
        self.emoji_class = kwargs.pop("emoji_class")
        self.emoji_src = kwargs.pop("emoji_src")

        super(EmojiInlineLexer, self).__init__(renderer, rules, **kwargs)

    def output_emoji(self, m):
        line = m.group(0)
        text = m.group(1)

        link = "{}/{}".format(self.emoji_src, self.emojis[text])

        if text in self.emojis:
            return self.renderer.image(link, text, text)

        return self.renderer.text(line)
