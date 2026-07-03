from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = r'G:\Program Files\Ai_CSX\rag_practice\data\files\历史文化.txt'


# 1.加载文档
#txt加载要加上编码格式
loader = TextLoader(file_path=file_path, encoding='utf-8')
docs = loader.load()

# 2.文本拆分
splitter = RecursiveCharacterTextSplitter(
    chunk_size=55,
    chunk_overlap=8,
    separators=["\n\n", "\n", "。", "，", "、", " ", ""],
    #按照长度去分割就是len，有些时候按照token拆分
    length_function=len
)
chunks = splitter.split_text(docs[0].page_content)
#enumrate() 加个序号
for i, chunk in enumerate(chunks):
    print(f"--- 块 {i + 1} (长度: {len(chunk)}) ---")
    print(chunk)
    print()