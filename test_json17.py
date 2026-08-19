import re
import subprocess
res = subprocess.run(['git', 'show', 'origin/main:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
lines = res.stdout.split('\n')
for i, line in enumerate(lines):
    if '"blocks"' in line:
        print(f"Line {i}: {line}")
