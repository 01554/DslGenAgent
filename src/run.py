from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import yaml
import os

def create_workflow_plan(user_input: str) -> str:
    """ユーザー入力から計画書を生成"""
    with open("src/prompt/workflow_planner.md", "r") as f:
        planner_template = f.read()
    
    planner = LLMChain(
        llm=ChatOpenAI(temperature=0),
        prompt=PromptTemplate(
            template=planner_template,
            input_variables=["user_input"]
        )
    )
    return planner.run(user_input=user_input)

def collect_edge_info(plan: str) -> str:
    """計画書からエッジ情報を収集"""
    with open("src/prompt/edge_collection.md", "r") as f:
        collector_template = f.read()
    
    collector = LLMChain(
        llm=ChatOpenAI(temperature=0),
        prompt=PromptTemplate(
            template=collector_template,
            input_variables=["plan"]
        )
    )
    return collector.run(plan=plan)

def generate_edges(edge_info: str) -> dict:
    """エッジ情報からワークフローのエッジ部分を生成"""
    with open("src/prompt/edge_generator.md", "r") as f:
        generator_template = f.read()
    
    generator = LLMChain(
        llm=ChatOpenAI(temperature=0),
        prompt=PromptTemplate(
            template=generator_template,
            input_variables=["edge_info"]
        )
    )
    return yaml.safe_load(generator.run(edge_info=edge_info))

def collect_node_info(plan: str) -> str:
    """計画書からノード情報を収集"""
    with open("src/prompt/node_collection.md", "r") as f:
        collector_template = f.read()
    
    collector = LLMChain(
        llm=ChatOpenAI(temperature=0),
        prompt=PromptTemplate(
            template=collector_template,
            input_variables=["plan"]
        )
    )
    return collector.run(plan=plan)

def generate_nodes(node_info: str) -> dict:
    """ノード情報からワークフローのノード部分を生成"""
    with open("src/prompt/node_generator.md", "r") as f:
        generator_template = f.read()
    
    generator = LLMChain(
        llm=ChatOpenAI(temperature=0),
        prompt=PromptTemplate(
            template=generator_template,
            input_variables=["node_info"]
        )
    )
    return yaml.safe_load(generator.run(node_info=node_info))

def main(user_input: str):
    # 1. 計画書作成
    plan = create_workflow_plan(user_input)
    
    # 2-3. エッジ情報の収集と生成
    edge_info = collect_edge_info(plan)
    edges = generate_edges(edge_info)
    
    # 4-5. ノード情報の収集と生成
    node_info = collect_node_info(plan)
    nodes = generate_nodes(node_info)
    
    # 6. 統合
    workflow = {
        "nodes": nodes,
        "edges": edges
    }
    
    # 結果の出力
    with open("output/workflow.yml", "w") as f:
        yaml.dump(workflow, f)

if __name__ == "__main__":
    main("入力された画像を元に俳句を読むワークフローを生成")
