import re 
# Content cleaner


URLS_FOLDER = r"folderpath"

EXCLUDED_DOMAINS = [
     "facebook.com", "tiktok.com", "twitter.com", "linkedin.com",
    "reddit.com", "vimeo.com", "brainly.com", "pinterest.com", "instagram.com"
]

class DataProcessor:
    NEGATIVE_CONTENT_PATTERN = re.compile(
        r"(subscribe|newsletter|cookie|consent|related posts|related articles|quick links|back to top|"
        r"explore related topics|speak with a specialist|small business services|bizfilings|comparison chart|"
        r"learn more|related insights|webinar|compliance|visit our|home page|current page|navigation|"
        r"share|preferences|manage consent|statistics|functional always active|marketing purposes|unsubscribe|footer)",
        re.IGNORECASE
    )

    @staticmethod
    def extract_main_content(markdown):
        markdown = re.sub(r'!\[.*?\]\(.*?\)', '', markdown)
        markdown = re.sub(r'\[.*?\]\(.*?\)', '', markdown)
        markdown = re.sub(r'<(nav|footer|header|aside).*?>.*?</\1>', '', markdown, flags=re.DOTALL|re.IGNORECASE)
        markdown = re.sub(r'(##+\s?(Table of Contents|Contents|Related Posts|See Also|Further Reading|Explore related topics).*?)(##|\Z)',
                          '', markdown, flags=re.DOTALL | re.IGNORECASE)
        markdown = re.sub(r'This (website|site) uses cookies.*?accept\.', '', markdown, flags=re.IGNORECASE | re.DOTALL)
        markdown = re.sub(r'(subscribe.*?newsletter.*?)\n+', '', markdown, flags=re.IGNORECASE | re.DOTALL)
        markdown = re.sub(r'(manage consent.*?)\n+', '', markdown, flags=re.IGNORECASE | re.DOTALL)
        markdown = re.sub(r'(accept cookies.*?)\n+', '', markdown, flags=re.IGNORECASE | re.DOTALL)
        markdown = re.sub(r'https?://\S+', '', markdown)
        markdown = re.sub(r'\[.*?\]', '', markdown)
        markdown = re.sub(r'---.*?---', '', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<.*?>', '', markdown)

        filtered_lines = []
        for line in markdown.split('\n'):
            if DataProcessor.NEGATIVE_CONTENT_PATTERN.search(line):
                continue
            if len(line.strip()) == 0:
                continue
            filtered_lines.append(line)

        markdown = '\n'.join(filtered_lines)
        markdown = re.sub(r'\n\s*\n', '\n', markdown)
        return markdown.strip()


        
def extract_markdown_sections(markdown_text):
    sections = []
    current_section = {"heading": "", "content": ""}
    lines = markdown_text.split("\n")
    for line in lines:
        heading_match = re.match(r'^(#{1,6})\s*(.*)', line)
        if heading_match:
            if current_section["heading"] or current_section["content"]:
                current_section["content"] = current_section["content"].strip()
                sections.append(current_section)
                current_section = {"heading": "", "content": ""}
            current_section["heading"] = heading_match.group(2).strip()
        else:
            current_section["content"] += line + "\n"
    if current_section["heading"] or current_section["content"]:
        current_section["content"] = current_section["content"].strip()
        sections.append(current_section)
    return sections
