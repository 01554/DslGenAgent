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
- ノードとtoolsで構成されるワークフロー
- 利用可能なノードとツールはノード一覧表、tools一覧表にあるもののみ
- 考えられる中で一番シンプルなパターンを出力
- マーメイド方式で出力
- 他の出力はしない、マーメイドのみ出力

# User Input
{{user_input}}