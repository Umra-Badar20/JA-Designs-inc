import os
from bs4 import BeautifulSoup
import re

# List of files to process
files = [
    'about.html',
    'contact.html',
    'index.html',
    'packages.html',
    'portfolio.html',
    'request-a-quote.html',
    'reviews.html',
    'services.html'
]

external_services = ['tawk.to', 'googletagmanager.com', 'google-analytics.com', 'zendesk.com', 'hubspot.com']

def clean_html_file(file_path):
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Remove specific <script> tags (Analytics, Chat, etc.)
    scripts_to_remove = []
    for script in soup.find_all('script'):
        src = script.get('src', '')
        if any(service in src for service in external_services):
            scripts_to_remove.append(script)
        elif script.string and any(service in script.string for service in ['Tawk_API', 'gtag', 'UA-', 'HubSpot']):
            scripts_to_remove.append(script)
            
    for script in scripts_to_remove:
        script.decompose()
        
    # 2. Remove WordPress-specific <link> tags and Feeds
    links_to_remove = []
    for link in soup.find_all('link'):
        href = link.get('href', '')
        rel = link.get('rel', [])
        
        # WP API links / Feeds
        if 'https://api.w.org/' in rel:
            links_to_remove.append(link)
        elif 'alternate' in rel and ('application/json+oembed' in link.get('type', '') or 'text/xml+oembed' in link.get('type', '') or 'application/rss+xml' in link.get('type', '')):
            links_to_remove.append(link)
        elif 'EditURI' in rel:
            links_to_remove.append(link)
        elif 'shortlink' in rel:
            links_to_remove.append(link)
        elif 'wlwmanifest' in rel:
            links_to_remove.append(link)
        # Aggressive feed removal check
        if 'feed' in href and 'comments' in href:
            links_to_remove.append(link)
        elif '/feed/' in href:
             links_to_remove.append(link)

    for link in links_to_remove:
        link.decompose()
        
    # 3. Remove Generator Meta tag
    generators = soup.find_all('meta', attrs={'name': 'generator'})
    for gen in generators:
        if 'WordPress' in gen.get('content', ''):
            gen.decompose()

    # 4. Cleanup 'href' in <a> tags
    for a in soup.find_all('a', href=True):
        href = a['href']
        
        # If it points to order-form or backend actions
        if 'order-form' in href or 'contact.php' in href:
            a['href'] = '#'
        
        if 'wp-admin' in href or 'wp-login' in href:
            a['href'] = '#'

    # 5. Cleanup 'action' in <form> tags - AGGRESSIVE
    for form in soup.find_all('form', action=True):
        # Always neutralize actions for static site
        form['action'] = '#'
        
    # 6. Cleanup 'value' in <input> tags if they contain backend URLs (mostly for Gravity Forms hiddens)
    for inp in soup.find_all('input', value=True):
        val = inp['value']
        if 'wp-admin' in val or 'modevodesign.com' in val:
            inp['value'] = ''

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == "__main__":
    for file in files:
        if os.path.exists(file):
            clean_html_file(file)
        else:
            print(f"File not found: {file}")
            
    print("Cleanup complete.")
