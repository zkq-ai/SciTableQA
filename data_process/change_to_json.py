
import json

with open('../data/tableqa_data/zh-qa.txt') as f, \
    open('../data/tableqa_data/zh-qa.json', 'w', encoding='utf-8') as out:
    lines = f.read()
    lines = lines.replace('}\n{','},\n{')
    lines = '['+lines +']'
    data = json.loads(lines)
    json.dump(data, out, ensure_ascii=False, indent=4)