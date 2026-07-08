import hashlib

text = "你好，我想要学习Python 和 AI"
hash_value = hashlib.md5(text.encode('utf-8')).hexdigest()
#内容不变 所对应的hash值不变
print(hash_value)

text = "你好，我想 要学习Python 和 AI"
hash_value = hashlib.md5(text.encode('utf-8')).hexdigest()
print(hash_value)

