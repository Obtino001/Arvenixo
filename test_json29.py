with open('temp_origin_schema.json', 'r', encoding='utf-8') as f:
    s = f.read()

idx = s.find('"blocks": [')
print(s[idx:idx+1000])

print('\n\n--- END OF FILE ---')
print(s[-1000:])
