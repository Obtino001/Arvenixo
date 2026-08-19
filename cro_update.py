import json
import re

path = 'sections/main-product.liquid'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Insert rendering logic
render_html = '''              {%- when 'inventory_urgency' -%}
                {%- assign random_seed = product.id | modulo: 6 -%}
                {%- assign inventory_left = random_seed | plus: 4 -%}
                <div class="cro-inventory-urgency" {{ block.shopify_attributes }}>
                  <span class="cro-pulse-dot"></span>
                  <span class="cro-inventory-text">Only <strong>{{ inventory_left }}</strong> left in stock - order soon!</span>
                </div>
              {%- when 'countdown_timer' -%}
                <div class="cro-pdp-countdown" {{ block.shopify_attributes }}>
                  <div class="cro-countdown-inner">
                    <span class="cro-countdown-icon">
                      <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                    </span>
                    <span class="cro-countdown-text">{{ block.settings.text }}</span>
                    <span class="cro-countdown-timer" data-hours="{{ block.settings.hours }}">00h 00m 00s</span>
                  </div>
                </div>'''

if 'cro-inventory-urgency' not in c:
    # insert before {%- when 'buy_buttons' -%}
    c = c.replace("{%- when 'buy_buttons' -%}", render_html + '\n              {%- when \'buy_buttons\' -%}')

# 2. Insert into Schema
m = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', c, re.DOTALL)
if m:
    s = m.group(1)
    try:
        j = json.loads(s)
        
        # Check if blocks exist
        blocks = j.get('blocks', [])
        has_inventory = any(b.get('type') == 'inventory_urgency' for b in blocks)
        if not has_inventory:
            blocks.append({
                "type": "inventory_urgency",
                "name": "Urgency Inventory (CRO)",
                "limit": 1
            })
            blocks.append({
                "type": "countdown_timer",
                "name": "Countdown Timer (CRO)",
                "limit": 1,
                "settings": [
                    {
                        "type": "text",
                        "id": "text",
                        "default": "Order now for same day dispatch in:",
                        "label": "Text"
                    },
                    {
                        "type": "range",
                        "id": "hours",
                        "min": 1,
                        "max": 24,
                        "step": 1,
                        "label": "Reset hours (countdown duration)",
                        "default": 12
                    }
                ]
            })
            j['blocks'] = blocks
            new_schema = json.dumps(j, indent=2)
            c = c[:m.start()] + '{% schema %}\n' + new_schema + '\n{% endschema %}' + c[m.end():]
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            print("Successfully updated main-product.liquid schema and rendering!")
        else:
            print("Blocks already exist in schema!")
            
    except Exception as e:
        print("Schema JSON Parse Error:", e)
else:
    print("No schema found.")
