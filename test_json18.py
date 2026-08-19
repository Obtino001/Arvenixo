import re
import subprocess
res = subprocess.run(['git', 'show', 'origin/main:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
lines = res.stdout.split('\n')
for i in range(1910, 1920):
    print(f"Line {i}: {lines[i]}")
