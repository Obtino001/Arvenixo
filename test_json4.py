import json
import re
import subprocess
res2 = subprocess.run(['git', 'show', '7628c3c:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
c2 = res2.stdout
m2 = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', c2, re.DOTALL)
if m2:
    s2 = m2.group(1)
    lines = s2.split('\n')
    for i in range(953, 963):
        print(f"Line {i+1}: {lines[i]}")
