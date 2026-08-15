import re

with open('sections/store-features-static.liquid', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the 4 SVGs
svgs = re.findall(r'<svg.*?</svg>', content, re.DOTALL)

# Escape them for JSON
def escape_json(s):
    return s.replace('"', '\\"').replace('\n', ' ').replace('\r', '')

svg_1 = escape_json(svgs[0]) if len(svgs) > 0 else ''
svg_2 = escape_json(svgs[1]) if len(svgs) > 1 else ''
svg_3 = escape_json(svgs[2]) if len(svgs) > 2 else ''
svg_4 = escape_json(svgs[3]) if len(svgs) > 3 else ''

liquid_code = f'''<div class="custom-section7-index px-6 sm:px-10 lg:px-12 xl:px-16" {{{{ block.shopify_attributes }}}}>
  <div class="w-full mx-auto max-w-screen-full py-16 xs:py-20 sm:py-24 md:py-28 lg:py-32 xl:py-36 border-b relative">
    <div class="absolute top-12 xs:top-16 sm:top-20 w-full h-px bg-black md:hidden"></div>
    <div class="w-full md:w-5/6 lg:w-3/4 xl:w-2/3 mx-auto grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-5 lg:gap-6 xl:gap-8 text-[14px] sm:text-[18px] lg:text-[20px] xl:text-[24px]">
      
      {{%- for block in section.blocks -%}}
      <div class="col-span-1 text-center" {{{{ block.shopify_attributes }}}}>
        <a href="{{{{ block.settings.link | default: '#' }}}}" target="_blank" rel="noopener noreferrer">
          <div class="w-3/8 sm:w-3/10 md:w-4/9 mx-auto my-4 sm:my-6 lg:my-7 xl:my-8">
            {{{{ block.settings.svg_code }}}}
          </div>
          <h2 class="mb-1.5 sm:mb-2.5">
            {{{{ block.settings.title }}}}
          </h2>
          <span class="block w-max mx-auto font-light border-b">
            {{{{ block.settings.link_label }}}}
          </span>
        </a>
      </div>
      {{%- endfor -%}}
      
    </div>
  </div>
</div>

{{% schema %}}
{{
  "name": "Store Features Static",
  "tag": "section",
  "class": "section",
  "settings": [],
  "blocks": [
    {{
      "type": "feature",
      "name": "Feature",
      "settings": [
        {{
          "type": "html",
          "id": "svg_code",
          "label": "SVG Code"
        }},
        {{
          "type": "text",
          "id": "title",
          "label": "Heading",
          "default": "Feature Title"
        }},
        {{
          "type": "text",
          "id": "link_label",
          "label": "Link Label",
          "default": "Read"
        }},
        {{
          "type": "url",
          "id": "link",
          "label": "Link"
        }}
      ]
    }}
  ],
  "presets": [
    {{
      "name": "Store Features Static",
      "blocks": [
        {{
          "type": "feature",
          "settings": {{
            "title": "Worldwide Shipping",
            "link_label": "Read",
            "svg_code": "{svg_1}"
          }}
        }},
        {{
          "type": "feature",
          "settings": {{
            "title": "Worry-Free Purchase",
            "link_label": "Read",
            "svg_code": "{svg_2}"
          }}
        }},
        {{
          "type": "feature",
          "settings": {{
            "title": "30 Days Return",
            "link_label": "Read",
            "svg_code": "{svg_3}"
          }}
        }},
        {{
          "type": "feature",
          "settings": {{
            "title": "100% Secure Payments",
            "link_label": "Read",
            "svg_code": "{svg_4}"
          }}
        }}
      ]
    }}
  ]
}}
{{% endschema %}}
'''

with open('sections/store-features-static.liquid', 'w', encoding='utf-8') as f:
    f.write(liquid_code)

print('Successfully rewritten store-features-static.liquid')
