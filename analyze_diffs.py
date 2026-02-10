
import difflib

filename = r"c:\Users\PC\Documents\digitalsilk - Copy - Copy - Copy\css\style.css"

markers = {
    "about": 0,
    "contact": 39805, # Adjusted for 0-index based on previous scan (Line 39806 was 1-based)
    "graphic": 79610,
    "index": 119415,
    "law": 139383,
    "logo": 179188,
    "restaurant": 218993,
    "services": 258798,
    "migrated": 298602
}

# Read file lines
try:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

def get_block(start_line, end_line):
    return lines[start_line:end_line]

# Define block end points
block_ranges = [
    ("about", markers["about"], markers["contact"]),
    ("contact", markers["contact"], markers["graphic"]),
    ("index", markers["index"], markers["law"]), # Skip graphic for now
]

blocks = {}
for name, start, end in block_ranges:
    blocks[name] = get_block(start, end)
    print(f"Block {name}: {len(blocks[name])} lines")

# Compare About vs Contact
print("\nComparing About vs Contact...")
about_lines = blocks["about"]
contact_lines = blocks["contact"]

common_prefix_count = 0
min_len = min(len(about_lines), len(contact_lines))

for i in range(min_len):
    if about_lines[i] == contact_lines[i]:
        common_prefix_count += 1
    else:
        print(f"First mismatch at line {i}:")
        print(f"About: {about_lines[i].strip()}")
        print(f"Contact: {contact_lines[i].strip()}")
        break

print(f"Common prefix lines: {common_prefix_count}")
print(f"About lines remaining: {len(about_lines) - common_prefix_count}")
print(f"Contact lines remaining: {len(contact_lines) - common_prefix_count}")

# Check suffix?
common_suffix_count = 0
for i in range(1, min_len):
    if about_lines[-i] == contact_lines[-i]:
        common_suffix_count += 1
    else:
        break
print(f"Common suffix lines: {common_suffix_count}")
