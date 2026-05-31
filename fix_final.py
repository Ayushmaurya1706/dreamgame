
html = open('index.html', encoding='utf-8').read()

# Fix 1: Make scroll-info-panel visible by default (opacity 1 instead of 0)
html = html.replace(
    'opacity: 0;\n    transition: opacity 0.4s ease;',
    'opacity: 1;\n    transition: opacity 0.4s ease;'
)

# Fix 2: Update the CSS file too
css = open('index.css', encoding='utf-8').read()
css = css.replace(
    '    pointer-events: none;\n    opacity: 0;\n    transition: opacity 0.4s ease;',
    '    pointer-events: none;\n    opacity: 1;\n    transition: opacity 0.4s ease;'
)

# Fix 3: Update showInfoCard(0) to showInfoCard(1) in the < 0.12 branch 
# so card 1 is always visible even before scrolling
html = html.replace(
    "if (progress < 0.12) {\n            if (panel) panel.style.opacity = '0';\n            showInfoCard(0);",
    "if (progress < 0.12) {\n            if (panel) panel.style.opacity = '1';\n            showInfoCard(1);"
)

# Fix 4: show card 1 immediately on page load via inline style on sic-1
html = html.replace(
    '<div class="scroll-info-card" id="sic-1">',
    '<div class="scroll-info-card sic-active" id="sic-1">'
)

open('index.html', 'w', encoding='utf-8').write(html)
open('index.css', 'w', encoding='utf-8').write(css)
print("Done. HTML:", len(html), "CSS:", len(css))
