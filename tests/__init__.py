# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from flask import Flask

from flask_emoji import Emoji


class InitializationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

    def test_init_app(self):
        emoji = Emoji()
        emoji.init_app(self.app)

        self.assertIsInstance(emoji, Emoji)

    def test_class_init(self):
        emoji = Emoji(self.app)
        self.assertIsInstance(emoji, Emoji)
