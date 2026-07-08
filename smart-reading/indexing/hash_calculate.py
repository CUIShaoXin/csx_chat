import hashlib

class HashCalculate:
    """根据文件内容计算文件 hash"""
    def compute_hash(self, pdf_bytes: bytes) -> str:
        """从字节数据计算 MD5 哈希值"""
        return hashlib.md5(pdf_bytes).hexdigest()

    def compute_hash_from_file(self, file_path: str) -> str:
        """
        文件的大小 非常大 可能非常的大 不要 一次性读取 
        从文件路径计算 MD5 哈希值（流式读取）

        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()