from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

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
from src.util.edgesamples import EdgeSamples
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
    
def get_relation_edges(source_edge:Edge, workflowplan:WorkflowPlan) -> list[Edge]:
    # source_edge の ノードIDから、そのノードに接続されているエッジを取得
    source_node_id = source_edge.source_node_id
    relation_edges = [e for e in workflowplan.edges if e.target_node_id == source_node_id or e.source_node_id == source_node_id]
    return relation_edges


def main(user_request:str="テキストを受け取り（上限10000文字）、そのテキストから俳句を生成する", output_path:str="dsl.yml"):

    #llm_gpt4o_mini = ChatOpenAI(model="gpt-4o", temperature=0.0)
    """ DeepSeek Chatが重すぎて動かなくなっているので 一旦削除 Claudeを使用する 
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        openai_api_base="https://api.deepseek.com",
    )
    """
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        anthropic_api_key=os.getenv("CLAUDE_API_KEY"),
        max_tokens=8192,
        temperature=0.0,
    )
    

    # node_reference のディレクトリの構造からノードの一覧を生成
    node_list = NodeList().get_node_list()
    edge_samples = EdgeSamples().get_edge_samples()

    # ワークフローとエッジのつながりを生成
    workflowplan_generator = WorkflowPlanGenerator(llm)
    workflowplan = workflowplan_generator.generate_workflowplan(user_request, node_list, edge_samples)
    
    # エッジからノードを生成

    
    nodes = []  
    source_node_ids = []
    node_generator = NodeGenerator(llm)
    for edge in workflowplan.edges:
        src_node_type = edge.source_node_type.value
        src_node_id = edge.source_node_id
        src_description = edge.description

        node = node_generator.generate_node(src_node_type,src_node_id,src_description,get_relation_edges(edge, workflowplan),nodes)
        if node:
            nodes.append(node)
            source_node_ids.append(src_node_id)
        else:
            print(f"ノード生成に失敗しました。エッジ: {edge}")
            # TODO: ここでワークフロー生成からやりなおす

    for edge in workflowplan.edges:
        if edge.target_node_id not in source_node_ids:
            target_node_type = edge.target_node_type.value
            target_node_id = edge.target_node_id
            node = node_generator.generate_node(target_node_type,target_node_id,"",get_relation_edges(edge, workflowplan),nodes)
            if node:
                nodes.append(node)
    
    # ワークフローとノードを統合してDSLを生成
    dsl_generator = DSLGenerator(llm)
    dsl = dsl_generator.generate_dsl(user_request,workflowplan.edges,nodes)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(dsl)
