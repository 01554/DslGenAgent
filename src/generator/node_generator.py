import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.structure.edge import Edge
from typing import Optional

class NodeGenerator:
    def __init__(self, llm:ChatOpenAI):
        self.llm = llm
    def generate_node(self, source_edge: Edge, relation_edges: list[Edge]) -> Optional[str]: # Noneの場合はワークフロー生成からやり直し
        """
        エッジの情報を元にノードを生成
        """
        node_type = source_edge.source_node_type.value
        node_id = source_edge.source_node_id
        # node_reference ディレクトリの下に存在するか確認
        current_dir = os.path.dirname(os.path.abspath(__file__))
        node_reference_path = os.path.normpath(os.path.join(current_dir, "..", "..","node_reference"))
        
        if not os.path.exists(node_reference_path):
            return None
        
        #   node.yml を取得
        node_reference_path = f"{node_reference_path}/{node_type}/node.yml"
        with open(node_reference_path, 'r', encoding='utf-8') as f:
            node_reference = f.read()
        
        prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "あなたはノーコードツールDifyのDSLを作成する専門家です。",
            ),
            ('human', 
            "以下のエッジの情報を元に、node_id {node_id} のノードを生成してください。"
            "\n\nエッジ: {relation_edges}\n\n"
            "ノードの仕様は以下の通りです。\n{node_reference}"
            "\n<output_ref>はノードの出力を参照するためのものです。Promptのように書き換える必要があるものは書き換えること\n"
            "\n\n 出力は生成したyml部分のみ出力してください"
            )
            ]
        )
        chain = prompt | self.llm
        result = chain.invoke({"node_id":node_id, "relation_edges": relation_edges, "node_reference": node_reference})
        return result
    
    
