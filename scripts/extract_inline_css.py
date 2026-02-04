#!/usr/bin/env python3
import os
import hashlib
import re
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(__file__))
CSS_PATH = os.path.join(ROOT, 'css', 'style.css')
TARGET_FILES = [
    os.path.join(ROOT, 'index.html'),
    os.path.join(ROOT, 'about.html'),
    os.path.join(ROOT, 'contact.html'),
    os.path.join(ROOT, 'services.html'),
    os.path.join(ROOT, 'request-a-quote.html'),
]


def normalize_style(s):
    # Remove line breaks and extra spaces, ensure semicolon termination
    s = s.strip()
    s = re.sub(r"\s*;\s*", ";", s)
    s = re.sub(r"\s+", " ", s)
    if s and not s.endswith(";"):
        s = s + ";"
    return s


def ensure_link(soup):
    # Ensure link rel stylesheet exists and points to css/style.css
    head = soup.head
    if not head:
        return
    existing = head.find('link', rel='stylesheet')
    found = False
    for link in head.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if href.endswith('css/style.css'):
            found = True
            break
    if not found:
        # Insert link at end of head
        new_link = soup.new_tag('link', rel='stylesheet', href='css/style.css')
        head.append(new_link)


if __name__ == '__main__':
    from collections import OrderedDict

    style_blocks = []
    inline_map = OrderedDict()  # style_str -> class_name

    # Read existing css file
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, 'r', encoding='utf-8') as f:
            css_existing = f.read()
    else:
        css_existing = ''

    for path in TARGET_FILES:
        if not os.path.exists(path):
            print('Missing', path)
            continue
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

        # Extract and remove <style> blocks
        for style in soup.find_all('style'):
            text = style.string
            if text:
                normalized = text.strip() + "\n"
                if normalized not in style_blocks:
                    style_blocks.append(normalized)
            style.decompose()

        # Process inline style attributes
        for el in soup.find_all(attrs={"style": True}):
            style_val = el.get('style')
            norm = normalize_style(style_val)
            if not norm:
                del el['style']
                continue
            if norm not in inline_map:
                h = hashlib.md5(norm.encode('utf-8')).hexdigest()[:8]
                cls = f'inline-style-{h}'
                inline_map[norm] = cls
            cls = inline_map[norm]
            # add class
            existing_class = el.get('class', [])
            if cls not in existing_class:
                existing_class.append(cls)
            el['class'] = existing_class
            del el['style']

        # Ensure link
        ensure_link(soup)

        # Write back modified HTML
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print('Processed', path)

    # Append style blocks and generated classes to css file if not present
    additions = []
    for block in style_blocks:
        if block.strip() and block not in css_existing:
            additions.append(block)

    # Generate classes for inline styles
    if inline_map:
        inline_css = '\n/* Inline styles migrated from HTML */\n'
        for style_str, cls in inline_map.items():
            inline_css += f'.{cls} {{{style_str}}}\n'
        if inline_css not in css_existing:
            additions.append(inline_css)

    if additions:
        with open(CSS_PATH, 'a', encoding='utf-8') as f:
            f.write('\n/* ========== MIGRATED STYLES ========== */\n')
            for a in additions:
                f.write(a)
        print('Appended styles to', CSS_PATH)
    else:
        print('No new styles to append')
