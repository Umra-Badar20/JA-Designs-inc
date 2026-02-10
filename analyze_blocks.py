
import difflib

filename = r"c:\Users\PC\Documents\digitalsilk - Copy - Copy - Copy\css\style.css"

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

try:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

def get_block(start, end):
    # Normalize: strip content, ignore comments if possible (simple strip for now)
    return [l for l in lines[start:end]]

blocks = {
    "about": get_block(markers["about"], markers["contact"]),
    "contact": get_block(markers["contact"], markers["graphic"]),
    "index": get_block(markers["index"], markers["law"]),
    "services": get_block(markers["services"], markers["migrated"])
}

def compare(name1, name2):
    b1 = blocks[name1]
    b2 = blocks[name2]
    print(f"\nComparing {name1} ({len(b1)}) vs {name2} ({len(b2)}):")
    
    # Prefix
    prefix = 0
    limit = min(len(b1), len(b2))
    for i in range(limit):
        # Skip the first line content check (comment)
        if i == 0: 
            prefix += 1
            continue
        if b1[i] == b2[i]:
            prefix += 1
        else:
            print(f"  Diverges at line {i}:")
            print(f"  {name1}: {b1[i].strip()}")
            print(f"  {name2}: {b2[i].strip()}")
            break
    print(f"  Common Prefix: {prefix}")
    
    # Suffix
    suffix = 0
    for i in range(1, limit):
        if b1[-i] == b2[-i]:
            suffix += 1
        else:
            break
    print(f"  Common Suffix: {suffix}")

compare("about", "contact")
compare("about", "services")
compare("about", "index")
