import json
import re

# We will use the local header.liquid which has our HTML/JS/CSS injections but broken schema.
path = 'C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract the schema string (including broken syntax)
schema_match = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', content, re.DOTALL)
if schema_match:
    schema_str = schema_match.group(1)
    
    # Let's fix the schema using a known good schema structure.
    # The original issue was the duplication of the entire beginning up to mobile_logo_position.
    # Since I don't want to parse it manually, I'll just load the original json from git show origin/main:sections/header.liquid, fix the duplicate, load it as dict, insert my new fields, and write it back.
    
    import subprocess
    result = subprocess.run(['git', 'show', 'origin/main:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
    orig_content = result.stdout
    orig_match = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', orig_content, re.DOTALL)
    if orig_match:
        orig_schema = orig_match.group(1)
        # the original schema has a duplicate {% schema %} block inside mobile_logo_position!
        # It looks like: 
        #         {
        #           "value": "left",
        #           "label": "t:sections.header.settings.mobile_logo_position.options__2.label"
        # {% schema %}
        # {
        #   "name": "t:sections.header.name",
        # ...
        
        # We can split by {% schema %} and take the first part, then just close it?
        # NO! The first part is missing the rest of the settings!
        
        # Better idea: We just get the schema from another pristine Dawn theme?
        # OR we just grab the schema from Arvenixo/sections/header.liquid BEFORE I started, which I know is in 7628c3c!!!
        print('Checking out schema from 7628c3c...')
        res2 = subprocess.run(['git', 'show', '7628c3c:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
        c2 = res2.stdout
        m2 = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', c2, re.DOTALL)
        if m2:
            s2 = m2.group(1)
            try:
                schema_dict = json.loads(s2)
                print('7628c3c schema is VALID!')
                
                # Now we insert our fields
                # Find the "menu" setting in settings
                settings = schema_dict.get('settings', [])
                menu_idx = -1
                for i, s in enumerate(settings):
                    if s.get('id') == 'menu':
                        menu_idx = i
                        break
                
                if menu_idx != -1:
                    new_settings = [
                        {
                          "type": "header",
                          "content": "Mobile menu promo"
                        },
                        {
                          "type": "checkbox",
                          "id": "drawer_promo_enable",
                          "label": "Show promo card",
                          "default": True
                        },
                        {
                          "type": "image_picker",
                          "id": "drawer_promo_image",
                          "label": "Promo image"
                        },
                        {
                          "type": "text",
                          "id": "drawer_promo_title",
                          "label": "Promo title",
                          "default": "the skin bay club"
                        },
                        {
                          "type": "textarea",
                          "id": "drawer_promo_text",
                          "label": "Promo text",
                          "default": "get 10% off your next order, plus exclusive rewards every time you shop."
                        },
                        {
                          "type": "text",
                          "id": "drawer_promo_button",
                          "label": "Promo button",
                          "default": "read more"
                        },
                        {
                          "type": "url",
                          "id": "drawer_promo_link",
                          "label": "Promo link"
                        },
                        {
                          "type": "header",
                          "content": "Announcement Bar Socials"
                        },
                        {
                          "type": "text",
                          "id": "social_instagram",
                          "label": "Instagram URL"
                        },
                        {
                          "type": "text",
                          "id": "social_tiktok",
                          "label": "TikTok URL"
                        },
                        {
                          "type": "text",
                          "id": "social_facebook",
                          "label": "Facebook URL"
                        }
                    ]
                    
                    # insert after menu
                    settings = settings[:menu_idx+1] + new_settings + settings[menu_idx+1:]
                    schema_dict['settings'] = settings
                    
                    new_schema_str = json.dumps(schema_dict, indent=2)
                    
                    # Replace in file
                    new_content = content[:schema_match.start()] + '{% schema %}\n' + new_schema_str + '\n{% endschema %}' + content[schema_match.end():]
                    
                    with open(path, 'w', encoding='utf-8') as fout:
                        fout.write(new_content)
                        
                    print('Successfully replaced schema with valid JSON!')
                else:
                    print('Could not find menu setting.')
                    
            except Exception as e:
                print('Error parsing 7628c3c schema:', e)
