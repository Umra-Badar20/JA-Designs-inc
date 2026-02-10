
filename = r"c:\Users\PC\Documents\digitalsilk - Copy - Copy - Copy\css\style.css"

try:
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if "CSS from" in line or "/* =" in line:
                print(f"Line {i+1}: {line.strip()}")
            if i > 5000: # detailed scan for first 5000 lines? No, scan all, but limit output if too many.
                pass
except Exception as e:
    print(f"Error: {e}")
