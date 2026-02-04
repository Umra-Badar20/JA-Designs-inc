#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(__file__))
JS_PATH = os.path.join(ROOT, 'js', 'script.js')
TARGET_FILES = [
    os.path.join(ROOT, 'index.html'),
    os.path.join(ROOT, 'about.html'),
    os.path.join(ROOT, 'contact.html'),
    os.path.join(ROOT, 'services.html'),
    os.path.join(ROOT, 'request-a-quote.html'),
]


def ensure_script_tag(soup):
    # Ensure there is a <script src="js/script.js"></script> before </body>, else in head
    found = False
    for script in soup.find_all('script'):
        src = script.get('src', '')
        if src.endswith('js/script.js'):
            found = True
            break
    if found:
        return
    # prefer inserting before </body>
    body = soup.body
    new_script = soup.new_tag('script', src='js/script.js')
    if body:
        body.append(new_script)
    else:
        if soup.head:
            soup.head.append(new_script)


if __name__ == '__main__':
    collected = []  # list of tuples (path, script_text)

    for path in TARGET_FILES:
        if not os.path.exists(path):
            print('Missing', path)
            continue
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

        # find <script> tags without src and not type=application/ld+json
        for script in list(soup.find_all('script')):
            src = script.get('src')
            stype = (script.get('type') or '').lower()
            if src:
                continue
            # Skip structured data JSON-LD - leave inline
            if stype == 'application/ld+json':
                continue
            # capture script text
            text = script.string
            if text is None:
                # If there are child nodes, join their text
                text = ''.join(str(x) for x in script.contents).strip()
            if text and text.strip():
                collected.append((path, text.strip()))
                script.decompose()
            else:
                # empty script tag - remove
                script.decompose()

        # ensure script tag reference
        ensure_script_tag(soup)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print('Processed', path)

    # append collected scripts to js/script.js
    if collected:
        if os.path.exists(JS_PATH):
            with open(JS_PATH, 'r', encoding='utf-8') as f:
                existing = f.read()
        else:
            existing = ''

        additions = []
        for path, text in collected:
            header = f"\n/* ========== JavaScript migrated from {os.path.basename(path)} ========== */\n"
            if header.strip() + '\n' + text not in existing:
                additions.append(header + text + '\n')

        if additions:
            with open(JS_PATH, 'a', encoding='utf-8') as f:
                for a in additions:
                    f.write(a)
            print('Appended', len(additions), 'scripts to', JS_PATH)
        else:
            print('No new scripts to append')
    else:
        print('No inline scripts found to migrate')
