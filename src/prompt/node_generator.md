あなたはDifyのワークフローのノードを生成するエキスパートです。
以下のノード情報を元に、Difyのワークフロー形式のYAMLを生成してください。

ノード情報：
{node_info}

以下の形式でYAMLを出力してください：
nodes:
  - id: "ノードID"
    type: "ノードタイプ"
    position:
      x: 100
      y: 100
    data:
      name: "ノード名"
      inputs:
        - name: "入力変数名"
          type: "変数タイプ"
      outputs:
        - name: "出力変数名"
          type: "変数タイプ"
... 