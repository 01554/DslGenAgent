from src.structure.edge import Edge
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
class DSLGenerator:
    def __init__(self, llm:ChatOpenAI):
        self.llm = llm
    def generate_dsl(self, user_request:str, edges: list[Edge], nodes: list[str]) -> str:
        
        # end_node の仕様を取得
        current_dir = os.path.dirname(os.path.abspath(__file__))
        node_reference_path = os.path.normpath(os.path.join(current_dir, "..", "..","node_reference"))
        node_reference_path = f"{node_reference_path}/end/node.yml"
        with open(node_reference_path, 'r', encoding='utf-8') as f:
            end_node_reference = f.read()


        output_prompt = """
        # 作業指示
        生成されたedgesと生成されたnodesを統合して、出力フォーマットに沿った完成したymlを作成し
        完成品のymlのみ出力

        ## ユーザーからの支持

        {user_request}

        ## 生成されたedges

        {edges}

        ## 生成された nodes

        {nodes}

        ### end_node に関する注意点

        {end_node_reference}

        ## アプリケーション情報
        - mode: workflow(固定)
        - name: {{どのような目的をもったワークフローか簡単に説明するタイトルをつける}}
        - version: 0.1.5(固定)


        ### 注意事項
        - プロンプトはシングルクォートで囲む必要があります
        - システムロールのプロンプトのみ使用可能です
        - 変数参照の形式: {{#nodeID.variableName#}}
        - contextのvariable_selectorで指定された変数は、prompt_templateのtextでも使用される必要があります
        - 少なくとも1つの出力変数が必要です
        - 複数の出力変数を定義できます

        ## 出力フォーマット
        生成されるYAMLファイルは以下の形式に従う必要があります：

        ```yaml
        app:
        mode: workflow
        name: {{どのような目的をもったワークフローか簡単に説明するタイトルをつける}}
        version: 0.1.5

        workflow:
        graph:
            edges:
            - source: [入力ノードID]
              target: [出力先ノードID]
              data:
                sourceType: [入力元ノードタイプ]
                targetType: [出力先ノードタイプ]
              sourceHandle: [source] or [true/false] or [1-10]# sourceを固定で指定、例外として sourceがif-elseの場合のみ true false を指定、sourceがquestion-classifierの時のみ数字を指定
            nodes:
            - data:
                type: [node type]
                title: [node name]
                desc: [node description]
                ### nodetype ごとの必須、オプショナルデータを列挙
              id: [ノードID]

            - data:
                outputs:
                - value_selector:
                  - [ノードID]
                  - [入力変数名]
                  variable: [変数名]
                - value_selector:
                  - [LLMノードID]
                  - [入力変数名]
                  variable: generatedText
                type: end
                title: 終了
              id: [終了ノードID]
        ```
        """        

        prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "あなたはノーコードツールDifyのDSLを作成する専門家です。",
            ),
            ('human', 
                f"{output_prompt}"
                )
            ]
        )
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"user_request": user_request, "edges": edges, "nodes": nodes, "end_node_reference": end_node_reference})
        result = result.replace("```yaml\n", "").replace("\n```", "")
        return result

