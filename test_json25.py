import json
import re

path = 'C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Let's completely wipe the existing schema and replace it with a good one.
# I will download Dawn's pristine header schema from GitHub or just build it dynamically.
# Actually, wait. I can just find the LAST {% schema %} and FIRST {% schema %}.
matches = list(re.finditer(r'{%\s*schema\s*%}', c))
if len(matches) > 0:
    print(f"Found {len(matches)} schema tags in the file!")
    
    # The actual schema string is whatever is between the FIRST {% schema %} and the LAST {% endschema %}
    start_idx = matches[0].end()
    end_matches = list(re.finditer(r'{%\s*endschema\s*%}', c))
    end_idx = end_matches[-1].start()
    
    schema_str = c[start_idx:end_idx]
    
    # To fix this, I will just extract settings by parsing it loosely.
    # No, I can't.
    
    # Let's fix the duplicate.
    if '{% schema %}' in schema_str:
        print("Duplicate schema found inside schema_str!")
        # just split by {% schema %} and take the SECOND part?
        # If the first part was interrupted, the second part might be the full schema!
        parts = re.split(r'{%\s*schema\s*%}', schema_str)
        # The second part has the "name": "t:..." etc.
        s = parts[-1]
        
        # fix the trailing comma
        s = s.replace('},,', '},')
        s = re.sub(r'\}\s*\]\s*\}\,\s*\]\s*\}$', '}\n  ]\n}', s.strip())
        s = re.sub(r'\}\s*\]\s*\}\s*\]\s*\}$', '}\n  ]\n}', s.strip())
        
        try:
            j = json.loads(s)
            print("Successfully parsed second part!")
            
            # insert settings
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
            settings = j.get('settings', [])
            menu_idx = -1
            for i, setting in enumerate(settings):
                if setting.get('id') == 'menu':
                    menu_idx = i
                    break
            
            if menu_idx != -1:
                settings = settings[:menu_idx+1] + new_settings + settings[menu_idx+1:]
                j['settings'] = settings
                new_schema_str = json.dumps(j, indent=2)
                
                # reconstruct file
                new_content = c[:matches[0].start()] + '{% schema %}\n' + new_schema_str + '\n{% endschema %}\n' + c[end_matches[-1].end():]
                with open(path, 'w', encoding='utf-8') as fout:
                    fout.write(new_content)
                print("SUCCESSFUL REWRITE")
                
        except Exception as e:
            print("Failed to parse second part:", e)
