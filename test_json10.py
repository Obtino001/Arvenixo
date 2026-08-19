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
    if idx != -1:
        close_idx = s.find('}', idx)
        if close_idx != -1:
            s = s[:close_idx+1] + '\n  ]\n}'
    
    try:
        j = json.loads(s)
    except json.JSONDecodeError as e:
        print("Char", e.pos)
        print("Context around char:")
        print(s[e.pos-100:e.pos+100])
