import os
from src.util.util import get_node_types_from_directory
class EdgeSamples():
    def __init__(self):
        self.__edge_samples = []

        for node_type in get_node_types_from_directory().keys():
            self.__edge_samples.append(self._generate_edge_sample(node_type))
    
    def get_edge_samples(self) -> list[str]:
        return self.__edge_samples


    def _generate_edge_sample(self,node_type: str) -> str:
        """
        ノードタイプに基づいてエッジのサンプルを取得する
        
        Args:
            node_type: ノードタイプ名（サブディレクトリ名）
        Returns:
            エッジのサンプル
        """

        current_dir = os.path.dirname(os.path.abspath(__file__))
        node_reference_path = os.path.normpath(os.path.join(current_dir, "..", "..", "node_reference"))

        use_case = f"{node_reference_path}/{node_type}/edges.yml"
        
        try:
            with open(use_case, 'r', encoding='utf-8') as f:
                description = f.read()
                        
            return f"\n\n# {node_type} edges_sample\n\n```{description}```"
            
        except FileNotFoundError:
            # 利用不可とする
            return f"\n\n# {node_type} edges_sample\n\n**なし**"
