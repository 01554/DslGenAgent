# 手順書

## 必要な構造

### アプリケーション情報
- mode: workflow(固定)
- name: ワークフローの名前
- version: 0.1.5(固定)

### ワークフローグラフ
#### エッジ
```yaml
- source: [startまたは入力元ノードID]
  target: [出力先ノードID]
  data:
    sourceType: [開始または入力元ノードタイプ]
    targetType: [出力先ノードタイプ]
```

#### ノード

##### 開始ノード
```yaml
- id: 一意のID
  type: start
  variables:
    # ファイル入力例
    - type: file
      variable: input_document
      label: document
      required: true
      max_length: 48
      allowed_file_types:
        - document
      allowed_file_upload_methods:
        - local_file
        - remote_url

    # 数値入力例
    - type: number
      variable: input_number
      label: number
      required: true
      min: 0
      max: 1000000

    # 段落入力例
    - type: paragraph
      variable: paragraph
      label: paragraph
      required: true
      max_length: 99999
      options: []

    # 短文テキスト入力例
    - type: text-input
      variable: short_text
      label: text-input
      required: true
      max_length: 48
      options: []
```

##### LLMノード
```yaml
- id: 一意のID
  type: llm
  model:
    - provider: openai
    - name: gpt-4o-mini
    - mode: chat
    - completion_params:
      - temperature: [0.0-1.0]
  prompt_template:
    - id: 一意のID（例：'prompt1'）
      role: system
      text: シングルクォートで囲まれたプロンプトテキスト
  context:
    - enabled: true
    - variable_selector: このノードで使用する変数を指定
  vision:
    - enabled: [true/false]
    - configs: # vision enabled true の時は必須
        detail: high
        variable_selector:
          - [画像入力元のノードID]
          - [画像入力元のvariable]
```

##### 終了ノード
```yaml
- id: 一意のID
  type: end
  outputs: # 出力変数の定義
    - input_data: 入力データ
    - generated_text: 生成されたテキスト
```

## 作成ガイド

### 注意事項
- ノードIDは一意

### 各ノードの使い方

#### 開始ノード
##### 用途
- ワークフローの開始点として機能
- ユーザー入力の受け付け
- 入力情報を変数として保存

##### 構造
- id: 一意のID（必須）
- type: start（固定）
- variables: 入力変数の配列（必須）
  - type: 変数タイプ（必須）
  - variable: 変数名（必須）
- label: 表示ラベル（必須）
- required: 入力が必須かどうか（必須）
- その他の設定（タイプに応じて）

##### 変数タイプ
- file（ファイル入力）
  - allowed_file_types: 許可されるファイルタイプ
    - document: ドキュメントファイル
    - image: 画像ファイル
    - audio: 音声ファイル
    - video: 動画ファイル
  - allowed_file_upload_methods: アップロード方法
    - local_file: ローカルファイル
    - remote_url: リモートURL
  - max_length: ファイル名の最大長
  - required: フィールドが必須かどうか
- number（数値入力）:
  - min: 最小値（オプション）
  - max: 最大値（オプション）
- paragraph（段落テキスト）
  - max_length: 最大文字数（オプション）
  - options: オプション（オプション）
- text-input（短文テキスト）
  - max_length: 最大文字数（オプション）
  - options: オプション（オプション）

#### LLMノード
##### 用途
- テキスト生成とレスポンス作成
- 入力テキストの処理と変換
- 質問への回答生成

##### 構造
- id: 一意のID（必須）
- type: llm（固定）
- model:（必須）
  - provider: openai（固定）
  - name: gpt-4o-mini（固定）
  - mode: chat（固定）
  - completion_params:
    - temperature: 0.0-1.0の値（必須）
- prompt_template:（必須）
  - role: system（固定）
  - text: プロンプトテキスト（必須）
- context:（必須）
  - enabled: true（固定）
  - variable_selector: 使用する変数を指定（必須）
- vision:（必須）
  - enabled: true/false（必須）

##### 注意事項
- プロンプトはシングルクォートで囲む必要があります
- システムロールのプロンプトのみ使用可能です
- 変数参照の形式: {{#nodeID.variableName#}}
- contextのvariable_selectorで指定された変数は、prompt_templateのtextでも使用される必要があります

#### 終了ノード
##### 用途
- ワークフローの終点として機能
- 処理結果の出力を定義
- 後続システムへのデータ受け渡し

##### 構造
- id: 一意のID（必須）
- type: end（固定）
- outputs:（必須）
- value_selector:（必須）
  - [nodeID]
  - [variableName]
- variable: 出力変数名（必須）

##### 注意事項
- 少なくとも1つの出力変数が必要です
- 複数の出力変数を定義できます

## 出力フォーマット
生成されるYAMLファイルは以下の形式に従う必要があります：

```yaml
app:
  mode: workflow
  name: [ワークフロー名]
  version: 0.1.5

workflow:
  graph:
    edges:
      - source: [入力ノードID]
        target: [出力先ノードID]
        data:
          sourceType: [入力元ノードタイプ]
          targetType: [出力先ノードタイプ]
        sourceHandle: [source] or [true/false] # if-else nodeの場合のみtrue/false
    nodes:
      - data:
          type: [node type]
          title: [node name]
        ### ワークフローグラフ > #### ノード
        に書かれた仕様に従い nodetype ごとの必須、オプショナルデータを列挙
        id: [ノードID]

      - data:
          type: end
          title: 終了
          outputs:
            - value_selector:
                - [ノードID]
                - [変数名]
              variable: inputData
            - value_selector:
                - [LLMノードID]
                - text
              variable: generatedText
          id: [終了ノードID]
```