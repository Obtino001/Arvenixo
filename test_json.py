import json
import re

with open('C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid', 'r', encoding='utf-8') as f:
    content = f.read()

# The schema is broken. Let's fix the specific errors we introduced.
# We had a double comma: '},,'
content = content.replace('},,', '},')

# And at the end, I replaced '}\n  ]\n}' which might have broken something.
# Let's just fix the trailing comma if there is one.

# Let's extract the schema string
schema_match = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', content, re.DOTALL)
if schema_match:
    schema_str = schema_match.group(1)
    # The error was at the end of the schema. Let's find out what it is.
    try:
        json.loads(schema_str)
        print("JSON is valid!")
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        # print context
        err_idx = e.pos
        start = max(0, err_idx - 100)
        end = min(len(schema_str), err_idx + 100)
        print(f"Context around error: {schema_str[start:end]}")
