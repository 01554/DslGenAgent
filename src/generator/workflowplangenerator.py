from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.structure.edges import Edges
import pprint
class WorkflowPlanGenerator:
    def __init__(self, llm:ChatOpenAI):
        self.structure_llm = llm.with_structured_output(Edges)
        self.llm = llm

    def generate_edges(self, user_request: str, node_list: list[str]) -> Edges:
        advanced_user_request_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたはノーコードツールDifyのDSLを作成する専門家です。",
                ),
                ('human',
                 "ユーザーリクエストを満たすための実行計画を立てます、リクエストを満たすために必要と思われるタスクを洗い出してください。"
                 "ユーザーリクエストはそのままでは不足していると感がれます、例えば「複数の」、とか「詳細な」、とか「具体的な」、とか「もっと」、とか「もっと詳細な」、と書いてある場合は"
                 "そのままでは不足していると考えられるため、貴方がその部分を具体化してふくらませてください。"
                 "\n\n#ユーザーリクエスト: {user_request}\n\n"
                 "## 出力の注意 \n"
                 "出力は、膨らませたリクエストの内容ののみにしてください\n"
                 "挨拶や閉めの言葉、思考の途中経過は不要です。\n"
                 "膨らませたリクエストの内容ののみを出力してください\n"
                 )
            ]
        )
        chain = advanced_user_request_prompt | self.llm
        result = chain.invoke({"user_request": user_request})
        advanced_user_request = result
        pprint.pprint(advanced_user_request.content)
        task_list_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたはノーコードツールDifyのDSLを作成する専門家です。",
                ),
                ('human',
                 "以下のユーザーリクエストを満たすために必要なタスクを洗い出して分解してください。\n"
                 "\n\n#ユーザーリクエスト: {advanced_user_request}\n\n"
                 "## 出力の注意 \n"
                 "タスクのリストのみ出力してください"
                 )
            ]
        )
        chain = task_list_prompt | self.llm
        result = chain.invoke({"advanced_user_request": advanced_user_request})
        task_list = result
        pprint.pprint(task_list.content)


        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたはノーコードツールDifyのDSLを作成する専門家です。",
                ),
                ('human', 
                "以下のタスクリストを満たすためにノード一覧から利用可能なノードを選び必要なワークフローを考えノードのつながりを生成してください。"
                "\n\n task list : {task_list}"
                "\n\nユーザーリクエスト: {advanced_user_request}\n\n"
                "##利用可能なノード一覧は以下の通りです。\n{node_list}"
                
                )

            ]
        )
        chain = prompt | self.structure_llm
        # ワークフローを生成
        result = chain.invoke({"advanced_user_request": advanced_user_request, "node_list": node_list, "task_list": task_list})
        edges : Edges = result



        return edges
