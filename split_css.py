
import os

filename = r"c:\Users\PC\Documents\digitalsilk - Copy - Copy - Copy\css\style.css"
output_dir = r"c:\Users\PC\Documents\digitalsilk - Copy - Copy - Copy\css"

# Block starts based on earlier analysis
markers = {
    "about": 0,
    "contact": 39805,
    "graphic": 79610,
    "index": 119415,
    "law": 139383,
    "logo": 179188,
    "restaurant": 218993,
    "services": 258798,
    "migrated": 298602
}

# The split point for Common Base vs Page Specific
# Line 12495 in 0-indexed list (which is line 12496 in file) is */ @charset...
# So Base is 0 to 12495.
base_end = 12495 

try:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 1. Create Base style.css
    base_css = lines[:base_end]
    with open(os.path.join(output_dir, "style.css"), 'w', encoding='utf-8') as f:
        f.writelines(base_css)
    print(f"Created style.css with {len(base_css)} lines.")

    # 2. Create Page CSS files
    # Only creating for pages we know requested: index, about, services, contact
    # For others, we might need to handle them later or create them now to be safe?
    # Helper to clean the start of the block (remove that artifact line)
    def clean_block(block_lines):
        # The first line of the divergence was "*/ @charset...", or similar.
        # We should probably strip that line if it looks like garbage.
        if block_lines and "charset" in block_lines[0]:
             return block_lines[1:]
        if block_lines and "*/" in block_lines[0]:
             return block_lines[1:]
        return block_lines

    # Index
    index_lines = lines[markers["index"] + base_end : markers["law"]]
    index_lines = clean_block(index_lines)
    with open(os.path.join(output_dir, "index.css"), 'w', encoding='utf-8') as f:
        f.writelines(index_lines)
    print(f"Created index.css with {len(index_lines)} lines.")

    # About
    # About block starts at 0, so its "remainder" is from base_end to markers["contact"]
    about_lines = lines[markers["about"] + base_end : markers["contact"]]
    about_lines = clean_block(about_lines)
    with open(os.path.join(output_dir, "about.css"), 'w', encoding='utf-8') as f:
        f.writelines(about_lines)
    print(f"Created about.css with {len(about_lines)} lines.")

    # Services
    services_lines = lines[markers["services"] + base_end : markers["migrated"]]
    services_lines = clean_block(services_lines)
    with open(os.path.join(output_dir, "services.css"), 'w', encoding='utf-8') as f:
        f.writelines(services_lines)
    print(f"Created services.css with {len(services_lines)} lines.")

    # Contact
    contact_lines = lines[markers["contact"] + base_end : markers["graphic"]]
    contact_lines = clean_block(contact_lines)
    with open(os.path.join(output_dir, "contact.css"), 'w', encoding='utf-8') as f:
        f.writelines(contact_lines)
    print(f"Created contact.css with {len(contact_lines)} lines.")

except Exception as e:
    print(f"Error: {e}")
