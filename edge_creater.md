
# ノード一覧表

| No | ノードタイプ | 説明 |
|----|--------------|------|
| 1  | start        | ワークフローの開始ノードです。入力データが入ります |
| 2  | end          | ワークフローの終了ノードです。出力データを入れます |
| 4  | llm          | 大規模言語モデルノードです。 |
| 5  | knowledge-retrieval | ナレッジ検索ノードです。 |
| 6  | question-classifier | 質問分類ノードです。 |
| 7  | if-else      | 条件分岐ノードです。 |
| 8  | code         | コード実行ノードです。 |
| 9  | template-transform | テンプレート変換ノードです。 |
| 10 | http-request | HTTPリクエストノードです。 |
| 12 | variable-aggregator | 変数集約ノードです。 |
| 13 | tool         | ツール実行ノードです。 |
| 14 | parameter-extractor | パラメータ抽出ノードです。 |
| 15 | iteration    | 反復ノードです。 |
| 16 | document-extractor | ドキュメント抽出ノードです。 |
| 17 | list-operator | リスト操作ノードです。 |
| 18 | iteration-start | 反復開始ノードです。 |

# tools一覧表
|1| jina_reader | 指定したURLをLLMが読みやすいtext形式に直します、URLもしくはPDFが入力可能 |
|2| tavily_search |  A powerful AI-native search engine and web content extraction tool that provides highly relevant search results and raw content extraction from web pages. |

---

# instructions

提供された要件に基づいて、以下の要素を含むワークフローを生成します

# required_structure
```yml
app_info:
- mode: workflowを指定
- name: 目的を表す名前を設定
- version: 0.1.5を使用

workflow_graph:
edges:
    - source: 開始ノードのID（例：'1731228343114'）
    target: LLMノードのID（例：'1731229438627'）
    data:
        sourceType: start
        targetType: llm
    - source: LLMノードのID（例：'1731229438627'）
    target: 終了ノードのID（例：'1731228345560'）
    data:
        sourceType: llm
        targetType: end
    - source: 質問分類器ノードのID
    sourceHandle: '1'  # 質問分類1用
    target: ターゲットノードID1
    targetHandle: target
    data:
        sourceType: question-classifier
        targetType: [ターゲットノードタイプ]
    - source: 質問分類器ノードのID
    sourceHandle: '2'  # 質問分類2用
    target: ターゲットノードID2
    targetHandle: target
    data:
        sourceType: question-classifier
        targetType: [ターゲットノードタイプ]
    - source: [IF/ELSEノードID]
    target: [ターゲットノードID]
    data:
        sourceType: if-else
        targetType: [ターゲットノードタイプ]
    sourceHandle: 'true'  # IF条件成立時
    - source: [IF/ELSEノードID]
    target: [別のターゲットノードID]
    data:
        sourceType: if-else
        targetType: [ターゲットノードタイプ]
    sourceHandle: 'false'  # ELSE条件時
    - source: [ツールノードID]
    target: [ターゲットノードID]
    data:
        sourceType: tool
        targetType: [ターゲットノードタイプ]
```
# output format
生成されるYAMLファイルは以下の形式に従ってください：
- ノードIDはユニークなIDである必要があります。
- ノードIDは1700000000000から始まる必要があります。
- ノードIDは1700000000000から1799999999999までの範囲である必要があります。


```yaml
app:
    mode: workflow
    name: [ワークフロー名]
    version: 0.1.5

workflow:
    graph:
        edges:
        # IF/ELSE分岐のエッジ例
        - source: [IF/ELSEノードID]
            target: [ターゲットノードID]
            data:
            sourceType: if-else
            targetType: [ターゲットノードタイプ]
            sourceHandle: 'true'  # IF条件成立時
        - source: [IF/ELSEノードID]
            target: [別のターゲットノードID]
            data:
            sourceType: if-else
            targetType: [ターゲットノードタイプ]
            sourceHandle: 'false'  # ELSE条件時


# User Input
```graph TD
    A[start: ワークフローの開始ノード] --> B[template-transform: テンプレート変換ノード]
    B --> C[end: ワークフローの終了ノード]
```