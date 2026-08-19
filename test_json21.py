import json
import re
import subprocess

res = subprocess.run(['git', 'show', 'origin/main:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
c = res.stdout

idx_dup = c.find('{% schema %}', c.find('{% schema %} ') + 10)
if idx_dup != -1:
    print('Found duplicate schema tag at', idx_dup)
    idx_end = c.find('        {\n          "value": "left",\n          "label": "t:sections.header.settings.mobile_logo_position.options__2.label"\n        }', idx_dup)
    
    if idx_end != -1:
        print('Found end of duplicate block!')
        # c = c[:idx_dup] + c[idx_end + len of that block?]
        # actually, the block ending at idx_end is the END of the duplicate chunk.
        # But wait! The first chunk had {% schema %} ... options__2.label"
        # The duplicate chunk had {% schema %} ... options__2.label" } ], "default": "center", ...
        
        # Let's just do a clean slate:
        # Instead of parsing, I will just extract clean_schema.json from ANOTHER theme (which failed due to encoding), or I will just write a small JSON fixer with ast.
        pass
