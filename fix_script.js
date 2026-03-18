const fs = require('fs');
const file = 'c:\\Users\\umrab\\OneDrive\\Desktop\\JA designs Inc\\JA-Designs-inc\\js\\script.js';

let text = fs.readFileSync(file, 'utf8');
// Remove BOM if present
if (text.charCodeAt(0) === 0xFEFF) {
  text = text.slice(1);
}

const starts = [];
const regex = /\{\s*"(prefetch|@context)"/g;
let match;
while ((match = regex.exec(text)) !== null) {
    starts.push(match.index);
}

const ranges = [];
for (const start of starts) {
    let lineStart = text.lastIndexOf('\n', start);
    if (lineStart === -1) lineStart = 0;
    const lineText = text.substring(lineStart, start);
    
    if (lineText.includes('/*') || lineText.includes('//')) continue;
    
    let braceCount = 0;
    let end = -1;
    let inString = false;
    let escape = false;
    
    for (let i = start; i < text.length; i++) {
        const c = text[i];
        if (escape) {
            escape = false;
            continue;
        }
        if (c === '\\') {
            escape = true;
            continue;
        }
        if (inString) {
            if (c === '"') inString = false;
        } else {
            if (c === '"') inString = true;
            else if (c === '{') braceCount++;
            else if (c === '}') {
                braceCount--;
                if (braceCount === 0) {
                    end = i;
                    break;
                }
            }
        }
    }
    if (end !== -1) ranges.push({start, end});
}

ranges.sort((a, b) => b.start - a.start);
let fixed = 0;
for (const {start, end} of ranges) {
    text = text.substring(0, start) + '/* ' + text.substring(start, end + 1) + ' */' + text.substring(end + 1);
    fixed++;
}

fs.writeFileSync(file, text, 'utf8');
console.log(`Fixed ${fixed} blocks`);
