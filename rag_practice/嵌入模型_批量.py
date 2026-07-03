from langchain_community.embeddings import DashScopeEmbeddings

# 创建嵌入模型对象，默认使用 text-embedding-v1
embedding_model = DashScopeEmbeddings()

# 批量处理多个文本
texts = ["猫坐在垫子上", "一只猫在垫子上休息", "今天天气很好"]
#批量处理就是documents（）
results = embedding_model.embed_documents(texts)

print(type(results))
print(len(results))
print(results[0])
print(results[1])
print(results[2])

