from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph

import operator
from typing import Annotated, Any, Optional

from dotenv import load_dotenv


from enum import Enum
import yaml
import os
from pprint import pprint

from src.util import util
from src.util.nodelist import NodeList

from src.structure.workflowplan import WorkflowPlan
from src.structure.edge import Edge

from src.generator.workflowplangenerator import WorkflowPlanGenerator
from src.generator.node_generator import NodeGenerator
from src.generator.dsl_generator import DSLGenerator

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "dslautogen"




def generate_node(edge: Edge,llm:ChatOpenAI) -> Optional[str]: # Noneの場合はワークフロー生成からやり直し
    """
    エッジの情報を元にノードを生成
    """
    node_type = edge.source_node_type.value
    # node_reference ディレクトリの下に存在するか確認
    node_reference_path = f"node_reference/{node_type}"
    if not os.path.exists(node_reference_path):
        return None
    
    #   node.yml を取得
    node_reference_path = f"{node_reference_path}/node.yml"
    with open(node_reference_path, 'r', encoding='utf-8') as f:
        node_reference = f.read()
    
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "あなたはノーコードツールDifyのDSLを作成する専門家です。",
        ),
        ('human', 
         "以下のエッジの情報を元に、ノードを生成してください。"
         "\n\nエッジ: {edge}\n\n"
         "ノードの仕様は以下の通りです。\n{node_reference}"
         "\n\n 出力は生成したyml部分のみ出力してください"
         )
        ]
    )
    # ペルソナ生成のためのチェーンを作成
    chain = prompt | llm
    result = chain.invoke({"edge": edge, "node_reference": node_reference})
    print(result)
    return result
    
    

def main(user_request:str="テキストを受け取り（上限10000文字）、そのテキストから俳句を生成する", output_path:str="dsl.yml"):

    llm_gpt4o_mini = ChatOpenAI(model="gpt-4o", temperature=0.0)

    # node_reference のディレクトリの構造からノードの一覧を生成
    node_list = NodeList().get_node_list()

    # ワークフローとエッジのつながりを生成
    workflowplan_generator = WorkflowPlanGenerator(llm_gpt4o_mini)
    workflowplan = workflowplan_generator.generate_workflowplan(user_request, node_list)
    # エッジからノードを生成
    node_generator = NodeGenerator(llm_gpt4o_mini)
    nodes = [n for n in (node_generator.generate_node(e) for e in workflowplan.edges) if n]
    
    # ワークフローとノードを統合してDSLを生成
    dsl_generator = DSLGenerator(llm_gpt4o_mini)
    dsl = dsl_generator.generate_dsl(workflowplan.edges,nodes)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(dsl)
