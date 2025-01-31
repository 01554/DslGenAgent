from src.structure.edge import Edge
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
class DSLGenerator:
    def __init__(self, llm:ChatOpenAI):
        self.llm = llm
    def extract_yaml_content(self, yml_content: str) -> str:
        #self._extract_yaml_content(yml_content, "```yaml", "```")
        return self._extract_yaml_content(yml_content, "app:", "```")

    def _extract_yaml_content(self, yml_content: str, start_marker:str, end_marker:str) -> str:
        
        start_index = yml_content.find(start_marker) 
        end_index = yml_content.find(end_marker, start_index)
        
        if start_index == -1 :
            return yml_content
        if end_index == -1:
            end_index = len(yml_content)
        
        yaml_content = yml_content[start_index:end_index].strip()
        return yaml_content

    def iteration_parentId(self, yaml:str) -> str:
        output_prompt = """
        # yml仕様
        - nodes: 以下に設定されるノードで の isInIteration が true の場合は parentId を指定しなければならない
        - parentId は iteration ノードのIDを指定する
        - parentId は id と同じインデントに配置する
        
        ### OK 例
        - data:
            type: iteration-start
            title: イテレーション開始
            desc: ''
            isInIteration: true
          parentId: iteration001
          id: iteration001start
          type: custom-iteration-start

        ### NG 例
        - data:
            type: iteration-start
            title: イテレーション開始
            desc: ''
            isInIteration: true
            parentId: iteration001
          id: iteration001start
          type: custom-iteration-start


        ### 作業対象データ
        {yaml}

        ### 作業指示
        - 作業対象データの中で isInIteration が true の場合は parentId が存在するか確認
        - parentId が存在しない場合は parentId を付与する
        - parentId は iteration ノードのIDを指定する
        - yml仕様に従って付与する
        - parentIdが存在するがインデントが違う場合も修正する

        ## 作業上の注意
        -  完成したymlのみ出力 
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
        result = chain.invoke({"yaml": yaml})
        return result


    def convert_carriage_return(self, yaml:str) -> str:
        output_prompt = """
        # 作業指示
        codeノードとLLMノードのpromptの中は改行を\\nで表現するように修正する
        NG例:
        - data:
            code: "def main(expanded_keywords: arg1) -> dict:
        return {{
            \\"result\\": result = arg1.split('\\n')
        }}"       

        OK例:
        - data:
            code: "\\ndef main(arg1: str) -> dict:\\n    result = arg1.split('\\n')\\n\\n\
            \\    return {{\\n        \\"result\\": result,\\n    }}\\n"
        
        ### 作業対象データ
        {yaml}

        ## 作業上の注意
        完成したymlのみ出力 
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
        result = chain.invoke({"yaml": yaml})
        result = result.replace("```yaml\n", "").replace("\n```", "")
        return result

    def tool_node_fix(self, yaml:str) -> str:
        output_prompt = """
        # 作業指示
        - type: tool_* はエッジの設定を type: tool になるように修正する
        例1: targetType: tool_article_node の場合は エッジの設定は targetType: tool になるよう変換する
        例2: sourceType: tool_title_node の場合は エッジの設定は sourceType: tool になるよう変換する
        例3： targetType: end の場合は toolが頭にないためそのまま end にする
             sourceType: start の場合は toolが頭にないためそのまま start にする
             targetType: code の場合は toolが頭にないためそのまま code にする
             sourceType: iteration の場合は toolが頭にないためそのまま iteration にする
             sourceType: iteration-start の場合は toolが頭にないためそのまま iteration-start にする

        ### 作業対象データ
        {yaml}

        ## 作業上の注意
        本来変換しないものまでtoolに修正した場合、あなたの会社に損害請求をします、注意して作業してください、あなたの作業は地球の未来を決めます
        出力前によく作業前と作業後のymlを比較してやり直すべきと判断したらやり直してください
        完成したymlのみ出力してください、
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
        result = chain.invoke({"yaml": yaml})
        result = result.replace("```yaml\n", "").replace("\n```", "")
        return result

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

        ## ユーザーからの指示

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
        - 文字列はダブルクォートで囲む必要があります
        - 文字列は改行が使えません、全て一行にして 改行は" \n"で表現しなさい
        - コードやPromptは特に注意して ダブルクォートで囲み、改行は"\n"に変換しなさい
        - 最終出力の前に添付されたedgesとnodesの数を数えて、出力ymlに展開した数とあっているか確認して、不足している場合はやり直しなさい
        - エッジのIDとnodeのIDはそれぞれ対応しています、各々が一致していることを確認しなさい
        - エッジのsourceとtargetはそれぞれnodeのIDと一致しています、各々が一致していることを確認しなさい
        - iteration ノードはtype iteration と type iteration-start 二つのノードを必要とする特殊ノードである
        - iterationの中で使うnodeには iteration_id: iterationノードのID をつけなければならない
        - iteration-startノードはiterationノードのIDを parentId: として指定しなければならない
        - iteration-start ノードは type: custom-iteration-start と type: iteration-start の二つのtypeを指定しなければならない

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
              id: [source_node_id]-source-[target_node_id]-target
              data:
                sourceType: [入力元ノードタイプ]
                targetType: [出力先ノードタイプ]
                isInIteration: [true/false] 
                iteration_id: [iteration_id] # isInIteration が trueの場合は必須、falseの場合は不要なので行ごと削除 
              sourceHandle: [source] or [true/false] or [1-10]# sourceを固定で指定、例外として sourceがif-elseの場合のみ true false を指定、sourceがquestion-classifierの時のみ数字を指定
              targetHandle: target # targetで固定
            type: custom # 固定
            zIndex: [0 or 1002] # デフォルト0 イテレーション内は 1002 にする
            ... 以下全ての edge を展開する


            nodes:
            - data:
                type: [node type]
                title: [node name]
                desc: [node description]
                isInIteration: false / true # デフォルトはfalse
                iteration_id: '1738232569563' # isInIteration が trueの場合は必須、falseの場合は不要なので行ごと削除 
                ### nodetype ごとの必須、オプショナルデータを列挙
              id: [ノードID]

            ... 同様の形式で全ての node を展開する

            - data:
                outputs:
                - value_selector:
                  - [ノードID]
                  - [入力変数名]
                  variable: [変数名]
                - value_selector:
                  - [ノードID]
                  - [入力変数名]
                  variable: [変数名]
                type: end
                title: 終了
              id: [終了ノードID]
            

            # iteration ノードはtype iteration と type iteration-start 二つのノードを必要とする特殊ノードである
            - data:
              type: iteration
              desc: ''
              error_handle_mode: terminated
              is_parallel: false
              iterator_selector:
              - '1738232449083'
              - result
              output_selector:
              - '1738286416418'
              - text
              output_type: array[string]
              parallel_nums: 10
              selected: false
              start_node_id: 1738232569563start
              title: イテレーション
            id: '1738232569563'
          - data:
              type: iteration-start # 固定 iteration-startには二つのTypeを指定しなければいけない
              desc: ''
              isInIteration: true
              selected: false
              title: ''
            draggable: false
            id: 1738232569563start
            parentId: '1738232569563'
            type: custom-iteration-start # 固定 iteration-startには二つのtypeの指定が必要

        ```
          # 作業の注意点
          完成品のymlのみ出力

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
        result = self.convert_carriage_return(result)
        result = self.tool_node_fix(result)
        result = self.iteration_parentId(result)

        result = self.extract_yaml_content(result)
        

        
        return result


