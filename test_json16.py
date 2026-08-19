import re
import subprocess
res = subprocess.run(['git', 'show', 'origin/main:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
if '"blocks"' in res.stdout:
    print('YES blocks')
else:
    print('NO blocks')
