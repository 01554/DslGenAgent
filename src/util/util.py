import os
# ノードタイプ用Enumを自動生成
def get_node_types_from_directory(node_reference_path:str = "node_reference"):
    """node_reference以下に存在するディレクトリ名が利用可能なnode_type"""
      # ディレクトリパスを適切に設定してください
    subdirs = [d for d in os.listdir(node_reference_path) 
              if os.path.isdir(os.path.join(node_reference_path, d))]
    return {subdir.replace("-", "_"): subdir for subdir in subdirs}