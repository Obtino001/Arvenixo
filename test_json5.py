import json
import re

path = 'C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

schema_match = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', content, re.DOTALL)
if schema_match:
    s = schema_match.group(1)
    
    # 1. Strip duplicated schema block if present
    if '{% schema %}' in s:
        s = s.split('{% schema %}')[0]
        # remove the trailing broken part
        idx = s.rfind('}')
        if idx != -1:
            s = s[:idx+1]
        # Close the settings array and object
        s += '\n  ]\n}'

    # 2. Fix double commas
    s = s.replace('},,', '},')

    # 3. Strip all trailing brackets and braces after the last valid setting }
    # Let's find the last '}' that has "default": 36 (which is padding_bottom)
    # Actually, let's just forcefully fix the end:
    s = re.sub(r'\}\s*\]\s*\}\,\s*\]\s*\}$', '}\n  ]\n}', s.strip())
    s = re.sub(r'\}\s*\]\s*\}\,$', '}\n  ]\n}', s.strip())
    s = re.sub(r'\}\s*\]\s*\}\s*\]\s*\}$', '}\n  ]\n}', s.strip())

    try:
        j = json.loads(s)
        new_schema = json.dumps(j, indent=2)
        new_content = content[:schema_match.start()] + '{% schema %}\n' + new_schema + '\n{% endschema %}' + content[schema_match.end():]
        with open(path, 'w', encoding='utf-8') as fout:
            fout.write(new_content)
        print('SUCCESS')
    except Exception as e:
        print('FAILED', e)
        # Try a more aggressive fix
        lines = s.split('\n')
        # ...
