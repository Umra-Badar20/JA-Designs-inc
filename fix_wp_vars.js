const fs = require('fs');
const packagesPath = String.raw`c:\Users\PC\Documents\digitalsilk - Copy - Copy - Copy\css\packages.css`;

const variableMappings = [
    { regex: /var\(--wp--preset--color--black\)/g, replacement: 'var(--primary-color2)' },
    { regex: /var\(--wp--preset--color--cyan-bluish-gray\)/g, replacement: '#abb8c3' }, // No direct map, keep hex or approximate
    { regex: /var\(--wp--preset--color--white\)/g, replacement: 'var(--primary-color3)' },
    { regex: /var\(--wp--preset--color--pale-pink\)/g, replacement: '#f78da7' },
    { regex: /var\(--wp--preset--color--vivid-red\)/g, replacement: 'var(--secondary-color2)' },
    { regex: /var\(--wp--preset--color--luminous-vivid-orange\)/g, replacement: 'var(--secondary-color2)' },
    { regex: /var\(--wp--preset--color--luminous-vivid-amber\)/g, replacement: 'var(--secondary-color5)' },
    { regex: /var\(--wp--preset--color--light-green-cyan\)/g, replacement: '#7bdcb5' },
    { regex: /var\(--wp--preset--color--vivid-green-cyan\)/g, replacement: '#00d084' },
    { regex: /var\(--wp--preset--color--pale-cyan-blue\)/g, replacement: '#8ed1fc' },
    { regex: /var\(--wp--preset--color--vivid-cyan-blue\)/g, replacement: 'var(--secondary-color6)' },
    { regex: /var\(--wp--preset--color--vivid-purple\)/g, replacement: 'var(--primary-color1)' },
    { regex: /var\(--wp--preset--color--accent\)/g, replacement: 'var(--primary-color1)' },
    { regex: /var\(--wp--preset--color--primary\)/g, replacement: 'var(--primary-color2)' },
    { regex: /var\(--wp--preset--color--secondary\)/g, replacement: '#6d6d6d' },
    { regex: /var\(--wp--preset--color--subtle-background\)/g, replacement: '#dcd7ca' },
    { regex: /var\(--wp--preset--color--background\)/g, replacement: '#f5efe0' }
];

try {
    let content = fs.readFileSync(packagesPath, 'utf8');

    variableMappings.forEach(mapping => {
        content = content.replace(mapping.regex, mapping.replacement);
    });

    console.log('Replacing broken WP variables...');
    fs.writeFileSync(packagesPath, content, 'utf8');
    console.log('Done.');
} catch (err) {
    console.error(err);
}
