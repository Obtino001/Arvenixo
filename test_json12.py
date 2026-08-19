import re

path = 'C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# The file currently has TWO {% schema %} tags!
# Let's find all indices of {% schema %}
schema_matches = list(re.finditer(r'{%\s*schema\s*%}', content))
if len(schema_matches) >= 2:
    print('Found multiple schemas!')
    idx1 = schema_matches[0].start()
    idx2 = schema_matches[1].start()
    
    # We want to keep everything up to idx2.
    # Wait! At idx2, the JSON string was interrupted inside mobile_logo_position!
    # Let's look at what is right before idx2.
    before_idx2 = content[idx2-100:idx2]
    print('Before idx2:')
    print(before_idx2)
    
    # The duplicate block ends where? It ends right after mobile_logo_position.options__2.label"
    # Let's find that string AFTER idx2
    search_str = '"t:sections.header.settings.mobile_logo_position.options__2.label"\n        }'
    idx3 = content.find(search_str, idx2)
    if idx3 != -1:
        end_of_duplicate = idx3 + len(search_str)
        print('Found end of duplicate at', end_of_duplicate)
        # So the real content should be:
        # content[:idx2] + content[end_of_duplicate:]
        new_content = content[:idx2] + content[end_of_duplicate:]
        
        # now we need to fix double commas
        new_content = new_content.replace('},,', '},')
        
        # and fix the end of schema
        new_content = re.sub(r'\}\s*\]\s*\}\,?\s*\]\s*\}\s*{%\s*endschema\s*%}', '}\n  ]\n}\n{% endschema %}', new_content)
        new_content = re.sub(r'\}\s*\]\s*\}\s*{%\s*endschema\s*%}', '}\n  ]\n}\n{% endschema %}', new_content)

        with open('temp_fixed_header.liquid', 'w', encoding='utf-8') as fout:
            fout.write(new_content)
        print('Wrote to temp_fixed_header.liquid')
    else:
        print('Could not find end of duplicate string')
