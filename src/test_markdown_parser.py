import unittest
from markdown_parser import extract_markdown_images, extract_markdown_links

class TestMarkdownParser(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/dfsjkFZ.png)"
        )
        self.assertListEqual(
            [
                ("image1", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "https://i.imgur.com/dfsjkFZ.png")
            ],
            matches
        )

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual(
            [("link", "https://www.example.com")],
            matches
        )

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with [link1](https://example1.com) and [link2](https://example2.com)"
        )
        self.assertListEqual(
            [
                ("link1", "https://example1.com"),
                ("link2", "https://example2.com")
            ],
            matches
        )

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_mixed_content(self):
        text = "Here's a [link](https://example.com) and an ![image](https://image.com)"
        link_matches = extract_markdown_links(text)
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("link", "https://example.com")], link_matches)
        self.assertListEqual([("image", "https://image.com")], image_matches)

    def test_extract_markdown_complex_urls(self):
        matches = extract_markdown_links(
            "Here's a [link](https://example.com/path?param=value#fragment)"
        )
        self.assertListEqual(
            [("link", "https://example.com/path?param=value#fragment")],
            matches
        )

if __name__ == "__main__":
    unittest.main()
