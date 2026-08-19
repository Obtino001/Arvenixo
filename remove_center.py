import re

path = 'assets/base.css'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Remove the block that sets centering
c = re.sub(r'  \.shopify-section \.title,[\s\S]*?text-align:\s*center;\s*margin-left:\s*auto;\s*margin-right:\s*auto;\s*}', '', c)
c = re.sub(r'  \.shopify-section \.button,[\s\S]*?justify-content:\s*center;\s*}', '', c)
c = re.sub(r'  \.shopify-section \.card__content,[\s\S]*?align-items:\s*center;\s*}', '', c)
c = re.sub(r'  \.shopify-section\s*\{\s*text-align:\s*center;\s*}', '', c)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

