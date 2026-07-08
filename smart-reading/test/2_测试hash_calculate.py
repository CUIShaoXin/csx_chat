from indexing.hash_calculate import HashCalculate


hash_calculate = HashCalculate()
path = r'G:\Program Files\Ai_CSX\smart-reading\data\files\sample_document.pdf'
#只要文档路径不变  计算出来的hash值是一样的
print(hash_calculate.compute_hash_from_file(path))
print(hash_calculate.compute_hash_from_file(path))
print(hash_calculate.compute_hash_from_file(path))