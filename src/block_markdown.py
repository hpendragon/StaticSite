from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    # Split on double newlines
    blocks = markdown.split("\n\n")
    # Strip whitespace and filter out empty blocks
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def block_to_block_type(block):
    # Check for empty block
    if not block:
        raise ValueError("Empty block")

    # Check for heading (1-6 # characters followed by space)
    if block[0] == "#":
        heading_pattern = "# "
        for i in range(6):
            if block.startswith(heading_pattern):
                return BlockType.HEADING
            heading_pattern = "#" + heading_pattern
        # If we get here, it means we found a # but not followed by space
        return BlockType.PARAGRAPH

    # Check for code block (starts and ends with ```)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Split into lines for quote and list checking
    lines = block.split("\n")
    
    # Check for quote (every line starts with >)
    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE

    # Check for unordered list (every line starts with -)
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered list (lines start with 1., 2., etc.)
    if all(line.startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    # Default to paragraph
    return BlockType.PARAGRAPH
