import codecs
import re
import os

file_path = r'c:\Users\umrab\OneDrive\Desktop\JA designs Inc\JA-Designs-inc\js\script.js'

with codecs.open(file_path, 'r', 'utf-8-sig') as f:
    text = f.read()

starts = []
# Find all occurrences of {"prefetch" or {"@context" with optional spaces
for match in re.finditer(r'\{\s*"(prefetch|@context)"', text):
    starts.append(match.start())

ranges_to_comment = []
for start in starts:
    # Check if already in a comment by looking backwards to the beginning of the line
    line_start = text.rfind('\n', 0, start)
    if line_start == -1: line_start = 0
    line_text = text[line_start:start]
    
    # Simple heuristic to skip if it's already commented out
    if '/*' in line_text or '//' in line_text:
        continue
        
    brace_count = 0
    end = -1
    in_string = False
    escape = False
    
    # Parse to find matching closing brace
    for i in range(start, len(text)):
        c = text[i]
        
        if escape:
            escape = False
            continue
            
        if c == '\\':
            escape = True
            continue
            
        if in_string:
            if c == '"':
                in_string = False
        else:
            if c == '"':
                in_string = True
            elif c == '{':
                brace_count += 1
            elif c == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i
                    break

    if end != -1:
        ranges_to_comment.append((start, end))

# Sort the ranges in reverse order so replacements don't change earlier indices
ranges_to_comment.sort(key=lambda x: x[0], reverse=True)

fixed = 0
for s, e in ranges_to_comment:
    text = text[:s] + '/* ' + text[s:e+1] + ' */' + text[e+1:]
    fixed += 1

# Write back to file
with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(text)

print(f"Fixed {fixed} blocks.")
