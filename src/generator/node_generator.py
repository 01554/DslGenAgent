import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.structure.edge import Edge
from typing import Optional

class NodeGenerator:
    def __init__(self, llm:ChatOpenAI):
        self.llm = llm
    def generate_node(self, node_type:str, node_id:str, description:str, relation_edges: list[Edge],created_nodes:list[str]) -> Optional[str]: # Noneの場合はワークフロー生成からやり直し
        """
        エッジの情報を元にノードを生成
        """
        print(f"-------------------------------- generate_node {node_type} --------------------------------")
        
        # node_reference ディレクトリの下に存在するか確認
        current_dir = os.path.dirname(os.path.abspath(__file__))
        reference_path = os.path.normpath(os.path.join(current_dir, "..", "..","node_reference"))
        
        if not os.path.exists(reference_path):
            return None
        
        #   node.yml を取得
        node_reference_path = f"{reference_path}/{node_type}/node.yml"
        with open(node_reference_path, 'r', encoding='utf-8') as f:
            node_reference = f.read()
        #   use_case.yml を取得
        use_case_reference_path = f"{reference_path}/{node_type}/use_case.yml"
        with open(use_case_reference_path, 'r', encoding='utf-8') as f:
            use_case_reference = f.read()
        
        prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "あなたはノーコードツールDifyのDSLを作成する専門家です。",
            ),
            ('human', 
            "以下のエッジと作成済みノードの情報を元に、node_id {node_id} のノードを生成してください。\n"
            " このノードは {description} を実現するためのノードです"
            "\n\n関連エッジ: {relation_edges}\n\n"
            "作成済みのノード: {created_nodes}\n\n"
            "{node_type}の仕様は以下の通りです。\n{node_reference}"
            "\n<output_ref>はノード作成にあたり参考するためのものです。各項目で固定ではないものは全て適切な値に書き換えること\n"
            "\n<use_case>はノードの使用方法を参照するためのものです。\n{use_case_reference}"
            "\n\n 出力は生成したyml部分のみ出力してください"
            )
            ]
        )
        chain = prompt | self.llm
        result = chain.invoke({"node_id":node_id, "relation_edges": relation_edges,"created_nodes":created_nodes, "node_reference": node_reference, "use_case_reference": use_case_reference, "description": description, "node_type": node_type})
        return result
    
    
