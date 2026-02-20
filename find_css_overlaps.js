const fs = require('fs');
const path = require('path');

const stylePath = String.raw`c:\Users\PC\Documents\digitalsilk - Copy - Copy - Copy\css\style.css`;
const packagesPath = String.raw`c:\Users\PC\Documents\digitalsilk - Copy - Copy - Copy\css\packages.css`;

function extractSelectors(cssContent) {
    const selectors = new Set();
    let depth = 0;
    let currentSelector = '';
    let inComment = false;
    let i = 0;

    while (i < cssContent.length) {
        // Handle comments
        if (!inComment && cssContent.slice(i, i + 2) === '/*') {
            inComment = true;
            i += 2;
            continue;
        }
        if (inComment) {
            if (cssContent.slice(i, i + 2) === '*/') {
                inComment = false;
                i += 2;
            } else {
                i++;
            }
            continue;
        }

        const char = cssContent[i];

        if (char === '{') {
            if (depth === 0) {
                // End of selector(s)
                const parts = currentSelector.split(',');
                parts.forEach(p => {
                    const clean = p.trim();
                    if (clean && !clean.startsWith('@')) {
                        selectors.add(clean);
                    }
                });
                currentSelector = '';
            }
            depth++;
        } else if (char === '}') {
            depth--;
            if (depth < 0) depth = 0; // Should not happen in valid CSS
        } else {
            if (depth === 0) {
                currentSelector += char;
            }
        }
        i++;
    }
    return selectors;
}

try {
    const styleContent = fs.readFileSync(stylePath, 'utf8');
    const packagesContent = fs.readFileSync(packagesPath, 'utf8');

    const styleSelectors = extractSelectors(styleContent);
    const packagesSelectors = extractSelectors(packagesContent);

    const overlaps = [];
    packagesSelectors.forEach(s => {
        if (styleSelectors.has(s)) {
            overlaps.push(s);
        }
    });

    console.log(`Found ${overlaps.length} overlapping selectors.`);
    console.log(JSON.stringify(overlaps, null, 2));

} catch (err) {
    console.error('Error:', err);
}
