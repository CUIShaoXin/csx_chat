import json
import re


def extract_json(text):
    find_text = re.search(r"{.*}", text, re.DOTALL)
    if find_text:
        try:
            return json.loads(find_text.group(0))
        except json.JSONDecodeError:
            print(f"++++{text}++++不是一个合法的json格式")
    return None

s1 = '还记得发酒疯到:\n{"name":"张三","age":30}更多文本呢'
print(extract_json(s1))
