class MarkdownParser:
    def __init__(self, alt_text, start_index, end_index, url):
        self.alt_text = alt_text
        self.start_index = start_index
        self.end_index = end_index
        self.url = url

def extract_markdown_images(text):
    """
    Find all markdown images in the text and return a list of MarkdownParser objects
    containing the alt text, url, and position information
    """
    images = []
    curr_index = 0
    while curr_index < len(text):
        # Find the start of an image
        image_start = text.find("![", curr_index)
        if image_start == -1:
            break
            
        # Find the end of alt text
        alt_text_start = image_start + 2
        alt_text_end = text.find("]", alt_text_start)
        if alt_text_end == -1:
            break
            
        # Find the URL
        url_start = text.find("(", alt_text_end)
        if url_start == -1:
            break
        url_end = text.find(")", url_start)
        if url_end == -1:
            break
            
        # Extract the components
        alt_text = text[alt_text_start:alt_text_end]
        url = text[url_start + 1:url_end]
        
        # Create parser object
        image = MarkdownParser(
            alt_text=alt_text,
            start_index=image_start,
            end_index=url_end + 1,
            url=url
        )
        images.append(image)
        curr_index = url_end + 1
        
    return images

def extract_markdown_links(text):
    """
    Find all markdown links in the text and return a list of MarkdownParser objects
    containing the alt text, url, and position information
    """
    links = []
    curr_index = 0
    while curr_index < len(text):
        # Find the start of a link
        link_start = text.find("[", curr_index)
        if link_start == -1:
            break
            
        # Find the end of alt text
        alt_text_start = link_start + 1
        alt_text_end = text.find("]", alt_text_start)
        if alt_text_end == -1:
            break
            
        # Find the URL
        url_start = text.find("(", alt_text_end)
        if url_start == -1:
            break
        url_end = text.find(")", url_start)
        if url_end == -1:
            break
            
        # Extract the components
        alt_text = text[alt_text_start:alt_text_end]
        url = text[url_start + 1:url_end]
        
        # Create parser object
        link = MarkdownParser(
            alt_text=alt_text,
            start_index=link_start,
            end_index=url_end + 1,
            url=url
        )
        links.append(link)
        curr_index = url_end + 1
        
    return links
