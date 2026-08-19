import json
import re

path = 'C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', c, re.DOTALL)
if m:
    s = m.group(1)
    
    # fix the trailing comma I introduced earlier today
    s = s.replace('},,', '},')
    
    # Try parsing
    try:
        j = json.loads(s)
        print("Successfully parsed!")
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e)
        print("Context around error:")
        print(s[e.pos-100:e.pos+100])
