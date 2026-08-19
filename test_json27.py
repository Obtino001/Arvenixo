import json
import re

path = 'C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', c, re.DOTALL)
if m:
    s = m.group(1)
    s = s.replace('},,', '},')
    
    # We will just write the string to a temp file and use node to format it, it gives better errors!
    with open('temp_schema_for_node.json', 'w', encoding='utf-8') as fout:
        fout.write(s)
