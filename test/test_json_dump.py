import json

with open('../stats/data.json', 'w', encoding='utf-8') as f:
    data = {
        'a': 123,
        'foo': 'python 3'
    }
    json.dump(data, f, ensure_ascii=False, indent=2)
