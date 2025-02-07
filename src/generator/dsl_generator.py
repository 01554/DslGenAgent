from src.structure.edge import Edge
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
import re

class DSLGenerator:
    def __init__(self, llm:ChatOpenAI):
        self.llm = llm


    def convert_tool_type(self, input_string:str) -> str:
        # tool_ で始まる値を tool に置換するパターン
        pattern = r'(type|sourceType|targetType):\s*tool_\w+'
        replacement = r'\1: tool'
        
        # 正規表現による置換を実行
        result = re.sub(pattern, replacement, input_string)
        return result
    
    def extract_yaml_content(self, yml_content: str) -> str:
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
    
    def output_check(self, yaml:str) -> str:
        # プロンプトファイルのディレクトリパスを取得
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_dir = os.path.join(current_dir, "output_check")
        
        # ディレクトリ内の全てのpromptファイルを処理
        for prompt_file in os.listdir(prompt_dir):
            if prompt_file.endswith('.prompt'):
                prompt_path = os.path.join(prompt_dir, prompt_file)
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    output_check_prompt = f.read()
                # 各プロンプトに対してLLMを実行
                print(f"---- output_check_prompt: {prompt_file}")
                yaml = self._output_check(output_check_prompt, yaml)
                yaml = self.extract_yaml_content(yaml)
        
        return yaml

    def _output_check(self, output_check_prompt:str, yaml:str) -> str:
        prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "あなたはノーコードツールDifyのDSLを作成する専門家です。",
            ),
            ('human', 
                f"{output_check_prompt}"
                )
            ]
        )
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"yaml": yaml})
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
        result = self.convert_tool_type(result) # tool_ で始まる値を tool に置換する

        result = self.output_check(result)
        result = self.extract_yaml_content(result)
        

        
        return result


