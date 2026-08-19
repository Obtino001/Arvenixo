import json
import re

path = 'C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

schema_match = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', content, re.DOTALL)
if schema_match:
    s = schema_match.group(1)
    
    # fix double comma
    s = s.replace('},,', '},')

    # find the padding_bottom block which is the last setting
    # "id": "padding_bottom",
    idx = s.rfind('"id": "padding_bottom"')
    if idx != -1:
        # find the closing brace for this block
        close_idx = s.find('}', idx)
        if close_idx != -1:
            # Everything after close_idx should just be closing the settings array and the main object
            s = s[:close_idx+1] + '\n  ]\n}'
    
    try:
        j = json.loads(s)
        new_schema = json.dumps(j, indent=2)
        new_content = content[:schema_match.start()] + '{% schema %}\n' + new_schema + '\n{% endschema %}' + content[schema_match.end():]
        with open(path, 'w', encoding='utf-8') as fout:
            fout.write(new_content)
        print('SUCCESS')
    except Exception as e:
        print('FAILED', e)
