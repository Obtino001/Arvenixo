import json
import re
import subprocess

res = subprocess.run(['git', 'show', 'origin/main:sections/header.liquid'], capture_output=True, text=True, encoding='utf-8')
c = res.stdout

# Find the second {% schema %}
first_schema = c.find('{% schema %}')
if first_schema != -1:
    idx_dup = c.find('{% schema %}', first_schema + 10)
    if idx_dup != -1:
        idx_end = c.find('        {\n          "value": "left",\n          "label": "t:sections.header.settings.mobile_logo_position.options__2.label"\n        }', idx_dup)
        
        c_fixed = c[:idx_dup] + c[idx_end:]
        
        m = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', c_fixed, re.DOTALL)
        if m:
            s = m.group(1)
            # Try to parse
            try:
                j = json.loads(s)
                print("Successfully parsed!!")
                
                # Now let's inject our new settings!
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
                    
                    # Now apply HTML/CSS/JS and Button!
                    c_final = c_fixed[:m.start()] + '\n{% schema %}\n' + new_schema_str + '\n{% endschema %}\n' + c_fixed[m.end():]
                    
                    with open('scratch_nlk_css.css', 'r', encoding='utf-8') as fcss:
                        css = fcss.read()
                    with open('scratch_nlk_html.html', 'r', encoding='utf-8') as fhtml:
                        html = fhtml.read()
                    with open('scratch_nlk_js.js', 'r', encoding='utf-8') as fjs:
                        js = fjs.read()
                        
                    button = '''      <button type="button" class="header__icon header__icon--menu header__icon--summary link focus-inset" onclick="toggleMenu()" aria-label="Open menu">
        <span>
          <svg class="icon icon-hamburger" aria-hidden="true" focusable="false" role="presentation" viewBox="0 0 18 16">
            <path d="M1 .5a.5.5 0 100 1h15.71a.5.5 0 000-1H1zM.5 8a.5.5 0 01.5-.5h15.71a.5.5 0 010 1H1A.5.5 0 01.5 8zm0 7a.5.5 0 01.5-.5h15.71a.5.5 0 010 1H1a.5.5 0 01-.5-.5z" fill="currentColor">
          </svg>
        </span>
      </button>'''
          
                    c_final = c_final.replace('</style>', '\n' + css + '\n</style>')
                    
                    # In my previous code, I injected HTML and JS right before {% schema %}.
                    # Since we added a newline before {% schema %} in c_final, we can replace that.
                    c_final = c_final.replace("\n{% schema %}\n", '\n' + html + '\n<script>\n' + js + '\n</script>\n{% schema %}\n')
                    
                    c_final = re.sub(r'if section\.settings\.menu != blank\s*render \'header-drawer\'\s*endif', r'if section.settings.menu != blank\n      endif\n    -%}\n    {%- if section.settings.menu != blank -%}\n' + button + '\n    {%- endif -%}\n    {%- liquid', c_final)
                    
                    with open('sections/header.liquid', 'w', encoding='utf-8') as fout:
                        fout.write(c_final)
                    
                    print("Everything written successfully! Ready to push.")
                    
                else:
                    print('Could not find menu setting.')
                    
            except json.JSONDecodeError as e:
                print('JSONDecodeError:', e)
