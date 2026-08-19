import json
import re

path = 'C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', c, re.DOTALL)
if m:
    s = m.group(1)
    
    # The file has a duplicate {% schema %} string inside it! Let's remove the literal string {% schema %} so it doesn't break liquid!
    s = s.replace('{% schema %}', '')
    
    # Fix the trailing comma
    s = s.replace('},,', '},')
    
    # Let's count brackets
    open_brackets = s.count('[')
    close_brackets = s.count(']')
    open_braces = s.count('{')
    close_braces = s.count('}')
    
    # Append missing brackets
    if open_brackets > close_brackets:
        s += '\n  ]' * (open_brackets - close_brackets)
    
    if open_braces > close_braces:
        s += '\n}' * (open_braces - close_braces)
        
    try:
        j = json.loads(s)
        print("Successfully parsed!!!")
        
        # write it back
        new_schema = json.dumps(j, indent=2)
        new_c = c[:m.start()] + '{% schema %}\n' + new_schema + '\n{% endschema %}' + c[m.end():]
        
        with open(path, 'w', encoding='utf-8') as fout:
            fout.write(new_c)
            
        print("File fixed and written!")
    except Exception as e:
        print("Parse failed:", e)
