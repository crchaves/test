import os
import json
import re
import unittest

class TestSite(unittest.TestCase):
    def setUp(self):
        self.index_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
        self.json_path = os.path.join(os.path.dirname(__file__), '..', 'params.json')

    def test_index_exists(self):
        self.assertTrue(os.path.isfile(self.index_path))

    def test_json_exists(self):
        self.assertTrue(os.path.isfile(self.json_path))

    def test_title(self):
        with open(self.index_path, 'r', encoding='utf-8') as f:
            html = f.read()
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1).strip(), 'Test by crchaves')

    def test_stylesheets_present(self):
        with open(self.index_path, 'r', encoding='utf-8') as f:
            html = f.read()
        for css in ['normalize.css', 'stylesheet.css', 'github-light.css']:
            self.assertIn(css, html)

    def test_github_links(self):
        with open(self.index_path, 'r', encoding='utf-8') as f:
            html = f.read()
        self.assertIn('https://github.com/crchaves/test', html)

    def test_json_fields(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        self.assertIn('name', data)
        self.assertIn('tagline', data)

if __name__ == '__main__':
    unittest.main()
