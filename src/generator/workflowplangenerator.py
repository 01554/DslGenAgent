from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.structure.workflowplan import WorkflowPlan
import pprint
class WorkflowPlanGenerator:
    def __init__(self, llm:ChatOpenAI):
        self.structure_llm = llm.with_structured_output(WorkflowPlan)

    def generate_workflowplan(self, user_request: str, node_list: list[str],edge_samples:list[str]) -> WorkflowPlan:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたはノーコードツールDifyのDSLを作成する専門家です。",
                ),
                ('human', 
                "以下のユーザーリクエストを満たすためにノード一覧から利用可能なノードを選び必要なワークフローを考えノードのつながりを生成してください。"
                "\n\nユーザーリクエスト: {user_request}\n\n"
                "##利用可能なノード一覧は以下の通りです。\n{node_list}"
                "\n\n##エッジのつながりのサンプルは以下の通りです\n"
                "{edge_samples}"
                
                )

            ]
        )
        chain = prompt | self.structure_llm
        # ワークフローを生成
        result = chain.invoke({"user_request": user_request, "node_list": node_list, "edge_samples": edge_samples})
        workflowplan : WorkflowPlan = result
        return workflowplan
