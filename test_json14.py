import re
import subprocess
res = subprocess.run(['git', 'show', '7628c3c:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
c = res.stdout
m = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', c, re.DOTALL)
if m:
    s = m.group(1)
    print(s[-200:])
