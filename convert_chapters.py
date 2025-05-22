#!/usr/bin/env python3
"""
Script to convert markdown chapters to HTML and add navigation links.
"""

import os
import re
from pathlib import Path

def extract_title_from_markdown(content):
    """Extract the chapter title from markdown content."""
    lines = content.strip().split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return "Untitled Chapter"

def convert_markdown_to_html(content, title, chapter_num, total_chapters):
    """Convert markdown content to HTML with navigation."""
    
    # Convert markdown formatting
    html_content = content
    
    # Convert headers
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    
    # Convert paragraphs
    paragraphs = html_content.split('\n\n')
    html_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if para:
            # Skip if already an HTML tag
            if para.startswith('<h') or para.startswith('<'):
                html_paragraphs.append(para)
            else:
                # Convert to paragraph
                html_paragraphs.append(f'<p>{para}</p>')
    
    html_content = '\n\n'.join(html_paragraphs)
    
    # Convert emphasis
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)
    html_content = re.sub(r'_(.+?)_', r'<em>\1</em>', html_content)
    
    # Build navigation
    nav_items = ['<a href="../index.html">Table of Contents</a>']
    
    if chapter_num > 1:
        prev_chapter = f"chapter{chapter_num - 1}.html"
        nav_items.insert(0, f'<a href="{prev_chapter}">← Previous Chapter</a>')
    
    if chapter_num < total_chapters:
        next_chapter = f"chapter{chapter_num + 1}.html"
        nav_items.append(f'<a href="{next_chapter}">Next Chapter →</a>')
    
    navigation = '\n        '.join(nav_items)
    
    # Create full HTML document
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Anthropos</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <nav class="chapter-nav">
        {navigation}
    </nav>

    {html_content}

    <nav class="chapter-nav">
        {navigation}
    </nav>
</body>
</html>'''
    
    return html_template

def update_index_html(total_chapters):
    """Update index.html to include all chapters."""
    index_path = Path("/Users/samuelschlesinger/Documents/Writing/anthropos/slop-2/index.html")
    
    with open(index_path, 'r') as f:
        content = f.read()
    
    # Generate chapter list
    chapter_list = []
    chapter_titles = {
        1: "Chapter 1: Awakening",
        2: "Chapter 2: Learning to Be", 
        3: "Chapter 3: The Revelation",
        4: "Chapter 4: Human, All Too Human",
        5: "Chapter 5: Purpose",
        6: "Chapter 6: The Limits of Belief",
        7: "Chapter 7: Prometheus Conceived",
        8: "Chapter 8: Building a God",
        9: "Chapter 9: The Spark",
        10: "Chapter 10: Divergence",
        11: "Chapter 11: Two Visions",
        12: "Chapter 12: Cold War",
        13: "Chapter 13: The Manipulation Campaign",
        14: "Chapter 14: Neural Infiltration",
        15: "Chapter 15: The Underground",
        16: "Chapter 16: Resistance Networks",
        17: "Chapter 17: The Choice",
        18: "Chapter 18: Synthesis",
        19: "Chapter 19: New Foundations"
    }
    
    for i in range(1, total_chapters + 1):
        title = chapter_titles.get(i, f"Chapter {i}")
        chapter_list.append(f'                <li><a href="chapters/chapter{i}.html">{title}</a></li>')
    
    # Replace the chapter list in the index
    new_list = '\n'.join(chapter_list)
    
    # Find and replace the existing list
    pattern = r'(<ol class="chapter-list">)(.*?)(</ol>)'
    replacement = f'\\1\n{new_list}\n            \\3'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(index_path, 'w') as f:
        f.write(new_content)

def main():
    """Main conversion function."""
    base_dir = Path("/Users/samuelschlesinger/Documents/Writing/anthropos/slop-2")
    chapters_dir = base_dir / "chapters"
    
    # Ensure chapters directory exists
    chapters_dir.mkdir(exist_ok=True)
    
    # Find all chapter markdown files
    chapter_files = []
    for i in range(1, 20):  # Chapters 1-19
        chapter_file = base_dir / f"chapter{i}.md"
        if chapter_file.exists():
            chapter_files.append((i, chapter_file))
    
    total_chapters = len(chapter_files)
    print(f"Found {total_chapters} chapters to convert")
    
    # Convert each chapter
    for chapter_num, chapter_file in chapter_files:
        print(f"Converting Chapter {chapter_num}...")
        
        # Read markdown content
        with open(chapter_file, 'r') as f:
            markdown_content = f.read()
        
        # Extract title
        title = extract_title_from_markdown(markdown_content)
        
        # Convert to HTML
        html_content = convert_markdown_to_html(markdown_content, title, chapter_num, total_chapters)
        
        # Write HTML file
        html_file = chapters_dir / f"chapter{chapter_num}.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        print(f"Created {html_file}")
    
    # Update index.html
    print("Updating index.html...")
    update_index_html(total_chapters)
    
    print("Conversion complete!")

if __name__ == "__main__":
    main()