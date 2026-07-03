from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import DashScopeEmbeddings

# 1.创建 Chroma 客户端
chroma = Chroma(
    persist_directory="./chroma_db",
    collection_name="test-collection",
    embedding_function=DashScopeEmbeddings()
)

# 2. 新增 document
data = [
    Document(page_content="猫坐在垫子上"),
    Document(page_content="一只猫在垫子上休息"),
    Document(page_content="今天天气很好")
]
chroma.add_documents(
    documents=data,
    ids=[f"id-{i}" for i in range(1, len(data) + 1)]
)

# 3.相似度查询（和mysql的where等值查询不一样，我们这里是基于相似度匹配）
user_query = '猫在哪？'
result = chroma.similarity_search(user_query, k=1)
print(type(result))
print(result)

# 4.根据id进行删除
chroma.delete("id-2")
# result = chroma.similarity_search(user_query, k=1)
# result = chroma.max_marginal_relevance_search()
print(result)



























