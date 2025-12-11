import unittest
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        md = "This is **bolded** paragraph\n\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n\n- This is a list\n- with items"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_type_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Test invalid heading (no space after #)
        self.assertEqual(block_to_block_type("#Invalid heading"), BlockType.PARAGRAPH)

    def test_block_type_code(self):
        block = "```\ndef hello_world():\n    print('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        # Test code block with language
        self.assertEqual(block_to_block_type("```python\nprint('Hello')\n```"), BlockType.CODE)

    def test_block_type_quote(self):
        self.assertEqual(block_to_block_type("> Single line quote"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type("> Multi-line\n> Block quote"),
            BlockType.QUOTE
        )
        # Test invalid quote (missing space after >)
        self.assertEqual(block_to_block_type(">Invalid quote"), BlockType.PARAGRAPH)

    def test_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("- Single item"), BlockType.UNORDERED_LIST)
        self.assertEqual(
            block_to_block_type("- Item 1\n- Item 2\n- Item 3"),
            BlockType.UNORDERED_LIST
        )
        # Test invalid list (missing space after -)
        self.assertEqual(block_to_block_type("-Invalid list"), BlockType.PARAGRAPH)

    def test_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Single item"), BlockType.ORDERED_LIST)
        self.assertEqual(
            block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"),
            BlockType.ORDERED_LIST
        )
        # Test invalid ordered list (wrong numbers)
        self.assertEqual(
            block_to_block_type("1. Item 1\n3. Item 2"),
            BlockType.PARAGRAPH
        )

    def test_block_type_empty(self):
        with self.assertRaises(ValueError):
            block_to_block_type("")

    def test_block_type_mixed_content(self):
        # These should all be paragraphs because they don't fully match any other type
        self.assertEqual(
            block_to_block_type("Some text\n> Mixed with quote"),
            BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("1. List\nMixed with text"),
            BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("- List\n1. Mixed types"),
            BlockType.PARAGRAPH
        )

if __name__ == "__main__":
    unittest.main()
