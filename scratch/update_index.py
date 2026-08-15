import json
import re

# Read the schema from the liquid file
with open('sections/store-features-static.liquid', 'r', encoding='utf-8') as f:
    content = f.read()

schema_match = re.search(r'{% schema %}(.*?){% endschema %}', content, re.DOTALL)
if schema_match:
    schema_json = json.loads(schema_match.group(1))
    preset_blocks = schema_json['presets'][0]['blocks']
    
    # Read index.json
    with open('templates/index.json', 'r', encoding='utf-8') as f:
        index_raw = f.read()
    
    # Remove Shopify comments
    index_raw = re.sub(r'/\*.*?\*/', '', index_raw, flags=re.DOTALL).strip()
    index_data = json.loads(index_raw)
    
    # Add blocks to store_features_static
    if "store_features_static" in index_data["sections"]:
        blocks_data = {}
        block_order = []
        
        for i, block in enumerate(preset_blocks):
            block_id = f"block_{i+1}"
            blocks_data[block_id] = block
            block_order.append(block_id)
            
        index_data["sections"]["store_features_static"]["blocks"] = blocks_data
        index_data["sections"]["store_features_static"]["block_order"] = block_order
        
        # Write back to index.json with the comment preserved
        final_json = "/*\n * ------------------------------------------------------------\n * IMPORTANT: The contents of this file are auto-generated.\n *\n * This file may be updated by the Shopify admin theme editor\n * or related systems. Please exercise caution as any changes\n * made to this file may be overwritten.\n * ------------------------------------------------------------\n */\n"
        final_json += json.dumps(index_data, indent=2)
        
        with open('templates/index.json', 'w', encoding='utf-8') as f:
            f.write(final_json)
        print("Successfully updated index.json with blocks.")
    else:
        print("store_features_static not found in index.json sections")
else:
    print("Schema not found in file")
