import json
import re
import subprocess

res = subprocess.run(['git', 'show', '7628c3c:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
content = res.stdout

schema_match = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', content, re.DOTALL)
if schema_match:
    s = schema_match.group(1)
    print("Open braces {:", s.count('{'))
    print("Close braces }:", s.count('}'))
    print("Open brackets [:", s.count('['))
    print("Close brackets ]:", s.count(']'))
