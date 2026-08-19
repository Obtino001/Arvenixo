import json
import re

with open('C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid', 'r', encoding='utf-8') as f:
    content = f.read()

schema_match = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', content, re.DOTALL)
if schema_match:
    schema_str = schema_match.group(1)

    # Let's clean it up manually
    # 1. Remove duplicate {% schema %} and following junk
    if '{% schema %}' in schema_str:
        print('Found duplicate schema inside schema!')
        schema_str = schema_str.split('{% schema %}')[0]
    
    # 2. Fix double commas
    schema_str = schema_str.replace('},,', '},')

    # 3. Fix the end of the schema string to be valid JSON
    # Find the last '}' that belongs to a setting
    idx = schema_str.rfind('}')
    # the string might end in }  ] }, ] } etc.
    # We will just use regex to strip all trailing junk and reconstruct it
    schema_str = re.sub(r'\}\s*\]\s*\}\,?\s*\]\s*\}$', '}', schema_str.strip())
    schema_str = re.sub(r'\}\s*\]\s*\}$', '}', schema_str.strip())
    schema_str = re.sub(r'\}\s*\]\s*\}\,$', '}', schema_str.strip())

    # Ensure it ends properly
    schema_str = schema_str.rstrip(', \n\t')
    
    # Now it might just be the end of the last setting object. We need to close the array and main object.
    # But wait, does it have blocks?
    
    # Let's try to extract settings and blocks with regex or just brace matching
    print('Let me just use json5 or robust parsing. Oh wait, I can just use a simple state machine.')

