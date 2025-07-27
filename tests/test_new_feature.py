import unittest
from meme_tracker.new_feature import new_feature

class TestNewFeature(unittest.TestCase):
    def test_feature(self):
        self.assertIsNone(new_feature())