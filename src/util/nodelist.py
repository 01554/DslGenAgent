import os
from src.util.util import get_node_types_from_directory
class NodeList():
    def __init__(self):
        self.__node_list = []

        for node_type in get_node_types_from_directory().keys():
            self.__node_list.append(self._generate_node_description(node_type))
    
    def get_node_list(self) -> list[str]:
        return self.__node_list


    def _generate_node_description(self,node_type: str) -> str:
        """
        ノードタイプに基づいて説明文を生成する
        
        Args:
            node_type: ノードタイプ名（サブディレクトリ名）
        Returns:
            生成された説明文
        """

        current_dir = os.path.dirname(os.path.abspath(__file__))
        node_reference_path = os.path.normpath(os.path.join(current_dir, "..", "..", "node_reference"))

        use_case = f"{node_reference_path}/{node_type}/use_case.yml"
        
        try:
            with open(use_case, 'r', encoding='utf-8') as f:
                description = f.read()
                        
            return f"# node_type: {node_type}\n## {node_type} description\n\n{description}"
            
        except FileNotFoundError:
            # 利用不可とする
            return f"# node_type: {node_type}\n## {node_type} description\n\n**利用不可**"
