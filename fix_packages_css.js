const fs = require('fs');
const path = require('path');

const packagesPath = String.raw`c:\Users\PC\Documents\digitalsilk - Copy - Copy - Copy\css\packages.css`;

// Selectors to remove (found in previous step as overlaps)
const selectorsToRemove = new Set([
    ':root',
    'body',
    'a',
    'button',
    'input',
    'textarea',
    'select',
    'hr',
    'table',
    'fieldset',
    'pre',
    'code',
    'blockquote',
    'samp',
    'kbd',
    'caption'
]);

// Colors to map
const colorMappings = [
    { regex: /#000000/gi, replacement: 'var(--primary-color2)' },
    { regex: /#cd2653/gi, replacement: 'var(--primary-color1)' },
    { regex: /#0693e3/gi, replacement: 'var(--secondary-color6)' },
    { regex: /#e03e2d/gi, replacement: 'var(--secondary-color2)' },
    { regex: /#ff0000/gi, replacement: 'var(--secondary-color2)' },
    // Also handle RGB values if they appear in packages.css (e.g. in gradients)
    // The file view showed some rgb() usages. 
    // rgb(6, 147, 227) is roughly #0693e3
    // rgb(155, 81, 224) 
    // Let's stick to the hex mostly, but perform a global replace.
];

function processCss(cssContent) {
    let newContent = '';
    let i = 0;
    let depth = 0;
    let currentSelector = '';
    let buffer = '';
    let inComment = false;

    // We will parse line by line or char by char? 
    // Char by char is safer for braces.

    // Actually, simply removing blocks for specific selectors is tricky if they are grouped.
    // e.g. "h1, h2, h3 { ... }"
    // If we want to remove h1, we should rewrite it to "h2, h3 { ... }".
    // given the file structure of packages.css (viewed earlier), it seems to have :root { ... } separately.
    // simple regex replace for the whole block might be easier if the formatting is consistent.
    // But a parser is more robust.

    // Let's use a simpler approach for the removal: 
    // Iterate through the string, capture blocks. If selector matches 'remove set', skip the block.

    while (i < cssContent.length) {
        // Comments
        if (!inComment && cssContent.slice(i, i + 2) === '/*') {
            let commentEnd = cssContent.indexOf('*/', i + 2);
            if (commentEnd === -1) commentEnd = cssContent.length;
            else commentEnd += 2;

            buffer += cssContent.slice(i, commentEnd);
            i = commentEnd;
            continue;
        }

        const char = cssContent[i];

        if (char === '{') {
            if (depth === 0) {
                // End of selector, start of block
                const selectors = currentSelector.split(',').map(s => s.trim());

                // Filter out selectors we want to remove
                const keptSelectors = selectors.filter(s => !selectorsToRemove.has(s));

                if (keptSelectors.length === 0) {
                    // Remove this entire block
                    // Advance i to end of matching bracket
                    let localDepth = 1;
                    i++;
                    while (i < cssContent.length && localDepth > 0) {
                        if (cssContent[i] === '{') localDepth++;
                        else if (cssContent[i] === '}') localDepth--;
                        i++;
                    }
                    // Reset buffer/currentSelector for next
                    currentSelector = '';
                    // buffer (which contained previous content or comments) stays.
                    // effectively skipped writing the block to buffer
                    continue;
                } else {
                    // Some selectors kept, or all kept
                    if (keptSelectors.length !== selectors.length) {
                        // We modified the selector string
                        currentSelector = keptSelectors.join(', ');
                    }
                    buffer += currentSelector + '{';
                    currentSelector = '';
                }
            } else {
                buffer += char;
            }
            depth++;
        } else if (char === '}') {
            buffer += char;
            depth--;
        } else {
            if (depth === 0) {
                currentSelector += char;
            } else {
                buffer += char;
            }
        }
        i++;
    }
    buffer += currentSelector; // trailing whitespace?

    return buffer;
}


try {
    let content = fs.readFileSync(packagesPath, 'utf8');

    // 1. Remove Overlaps
    // content = processCss(content); // Parsing CSS properly is hard with just this.
    // The previous analysis showed specific blocks for :root, body, etc.
    // Let's try a safer regex for the specific known offenders in packages.css
    // matching "selector { ... }"

    selectorsToRemove.forEach(sel => {
        // Regex to match "selector { ... }" handling minimal nesting
        // Note: packages.css from WP usually has :root { ...variables... }
        // We want to kill that.

        // Match literal selector followed by whitespace and {
        // Use a loop to handle nested braces roughly

        // Actually, let's use the raw string removal for valid blocks if possible.
        // But the parser above is decent for top-level removals.
        // Let's refine the parser logic above and use it.
    });

    // Re-implementing the parser logic inside 'processCss' cleanly
    content = processCss(content);

    // 2. Color Replacement
    colorMappings.forEach(mapping => {
        content = content.replace(mapping.regex, mapping.replacement);
    });

    console.log('Writing updated content to ' + packagesPath);
    fs.writeFileSync(packagesPath, content, 'utf8');
    console.log('Done.');

} catch (err) {
    console.error(err);
}
