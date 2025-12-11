#src/test_extract_title.py
import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")
    
    def test_title_with_spaces(self):
        markdown = "#    Spaced    Title    "
        self.assertEqual(extract_title(markdown), "Spaced    Title")
    
    def test_title_with_formatting(self):
        markdown = "# **Bold** Title"
        self.assertEqual(extract_title(markdown), "**Bold** Title")
    
    def test_title_not_first_line(self):
        markdown = "\nSome text\n# The Title\nMore text"
        self.assertEqual(extract_title(markdown), "The Title")
    
    def test_no_title(self):
        markdown = "No title here\nJust some text"
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_wrong_header_level(self):
        markdown = "## Secondary header"
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()
