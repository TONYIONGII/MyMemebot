import unittest
from meme_tracker.new_feature import new_feature

class TestNewFeature(unittest.TestCase):
    def test_success_case(self):
        self.assertEqual(new_feature(5), 10)
    
    def test_error_case(self):
        self.assertIsNone(new_feature("invalid"))