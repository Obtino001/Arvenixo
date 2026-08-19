import json
import re

path = 'C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

schema_match = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', content, re.DOTALL)
if schema_match:
    s = schema_match.group(1)
    s = s.replace('},,', '},')
    idx = s.rfind('"id": "padding_bottom"')
    print(s[idx-500:idx+200])
