import json
import re
import subprocess

# 1. Get original origin/main schema
res = subprocess.run(['git', 'show', 'origin/main:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
c = res.stdout
m = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', c, re.DOTALL)
if m:
    s = m.group(1)
    
    # 2. Fix duplicate block
    s = s.replace('{% schema %}', '')
    # The duplicate block in origin/main repeats the whole beginning up to mobile_logo_position
    # It looks like:
    #         {
    #           "value": "left",
    #           "label": "t:sections.header.settings.mobile_logo_position.options__2.label"
    # 
    # {
    #   "name": "t:sections.header.name",
    #
    # We can just use a regex to remove the duplicated chunk
    # The duplicated chunk starts right after "options__2.label"
    match = re.search(r'options__2\.label"(.*?)"name": "t:sections\.header\.name"', s, re.DOTALL)
    if match:
        print('Found duplicate block start!')
        # Let's just find the first occurrence of "options__2.label" and everything before it, and stitch it to the SECOND occurrence of options__2.label
        parts = s.split('"t:sections.header.settings.mobile_logo_position.options__2.label"')
        if len(parts) >= 3:
            print('Removing duplicated part')
            s = parts[0] + '"t:sections.header.settings.mobile_logo_position.options__2.label"' + parts[2]
            
    # 3. Fix the end of the schema
    # The end of the schema has: }, ] }
    s = re.sub(r'\}\s*\]\s*\}\,\s*\]\s*\}$', '}\n  ]\n}', s.strip())
    
    # 4. Try parsing it!
    try:
        j = json.loads(s)
        print("Successfully parsed repaired origin/main schema!")
        
        # 5. Insert new settings
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
        
        # 6. Replace in local header.liquid
        with open('C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid', 'r', encoding='utf-8') as f:
            local_content = f.read()
            
        local_match = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', local_content, re.DOTALL)
        if local_match:
            new_content = local_content[:local_match.start()] + '{% schema %}\n' + new_schema_str + '\n{% endschema %}' + local_content[local_match.end():]
            with open('C:/Users/Yasir/Pictures/world-of-comfort/Arvenixo/sections/header.liquid', 'w', encoding='utf-8') as fout:
                fout.write(new_content)
            print("Wrote repaired schema to local header.liquid!")
            
    except Exception as e:
        print('FAILED to parse repaired schema:', e)
