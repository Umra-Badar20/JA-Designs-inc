import os
import re

def main():
    base_dir = r'c:\Users\PC\Documents\digitalsilk'
    index_path = os.path.join(base_dir, 'index.html')
    
    # Files to process
    files_to_convert = ['contact.php', 'services.php', 'about.php']
    
    print(f"Reading index.html from {index_path}...")
    with open(index_path, 'r', encoding='utf-8') as f:
        index_lines = f.readlines()
        
    # Extract Header: from after <div class="wrapper"> up to before <main id="main-content"
    # wrapper is at line 106 (index 105)
    # main is at line 219 (index 218)
    # We want lines 107-218 (indices 106 to 218 exclusive)
    # Let's double check using content to be safe
    
    header_start_idx = -1
    header_end_idx = -1
    
    footer_start_idx = -1
    footer_end_idx = -1
    
    for i, line in enumerate(index_lines):
        if '<div class="wrapper">' in line and header_start_idx == -1:
            header_start_idx = i + 1
        if '<main id="main-content"' in line and header_end_idx == -1:
            header_end_idx = i
        if '</main>' in line:
            footer_start_idx = i + 1
        if '</body>' in line:
            footer_end_idx = i

    if header_start_idx == -1 or header_end_idx == -1 or footer_start_idx == -1 or footer_end_idx == -1:
        print("Error: Could not locate header/footer boundaries in index.html")
        return

    header_content = "".join(index_lines[header_start_idx:header_end_idx])
    footer_content = "".join(index_lines[footer_start_idx:footer_end_idx])
    
    print(f"Extracted Header ({len(index_lines[header_start_idx:header_end_idx])} lines)")
    print(f"Extracted Footer ({len(index_lines[footer_start_idx:footer_end_idx])} lines)")

    for filename in files_to_convert:
        file_path = os.path.join(base_dir, filename)
        if not os.path.exists(file_path):
            print(f"Skipping {filename} (not found)")
            continue
            
        print(f"Processing {filename}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace Header Include
        # regex for <?php include('header.php') ?> allowing for variations
        content = re.sub(r'<\?php\s+include\([\'"]header\.php[\'"]\)\s*\?>', header_content, content, flags=re.IGNORECASE)
        # Also try variations with semicolons
        content = re.sub(r'<\?php\s+include\([\'"]header\.php[\'"]\);\s*\?>', header_content, content, flags=re.IGNORECASE)

        # Replace Footer Include
        content = re.sub(r'<\?php\s+include\([\'"]footer\.php[\'"]\)\s*\?>', footer_content, content, flags=re.IGNORECASE)
        content = re.sub(r'<\?php\s+include\([\'"]footer\.php[\'"]\);\s*\?>', footer_content, content, flags=re.IGNORECASE)
        
        # Replace .php links with .html
        content = content.replace('.php"', '.html"')
        content = content.replace(".php'", ".html'")
        
        # Save as .html
        new_filename = filename.replace('.php', '.html')
        new_path = os.path.join(base_dir, new_filename)
        
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Saved {new_filename}")

if __name__ == '__main__':
    main()
