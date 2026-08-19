import re
import subprocess
res = subprocess.run(['git', 'show', 'origin/main:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
c = res.stdout
m = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', c, re.DOTALL)
if m:
    s = m.group(1)
    with open('temp_origin_schema.json', 'w', encoding='utf-8') as f:
        f.write(s)
