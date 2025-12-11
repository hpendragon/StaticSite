import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = "This is **bolded** paragraph text in a p tag here\n\nThis is another paragraph with _italic_ text and `code` here"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3 with _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <i>italic</i></h3></div>",
        )

    def test_quotes(self):
        md = "> This is a quote\n> with multiple lines\n> and **bold** text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- List item 1\n- List item 2 with **bold**\n- List item 3 with `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>List item 1</li><li>List item 2 with <b>bold</b></li><li>List item 3 with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. First item\n2. Second item with _italic_\n3. Third item with `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ol></div>",
        )

    def test_mixed_content(self):
        md = "# Main heading\n\nThis is a paragraph with **bold** text.\n\n> This is a quote with _italic_ text.\n\n- List item 1\n- List item 2\n\n```\nCode block here\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main heading</h1><p>This is a paragraph with <b>bold</b> text.</p><blockquote>This is a quote with <i>italic</i> text.</blockquote><ul><li>List item 1</li><li>List item 2</li></ul><pre><code>Code block here</code></pre></div>",
        )

    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

if __name__ == "__main__":
    unittest.main()
