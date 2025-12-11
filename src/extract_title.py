#src/extract_title.py
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    raise ValueError("No H1 header found in markdown file")
