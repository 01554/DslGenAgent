
# このプロジェクトについて
このプロジェクトは DifyのDSLを自動生成するためのプロジェクトです。

## Difyワークフロー自動生成界隈の課題
世の中に公開されているDifyの自動生成プロジェクトはいくつかのノード情報と少々のToolを含んだ一発Promptになっています。  
簡単なワークフローであればこれでも作成ができてしまうんですが、これだとDifyの能力を十全に生かしているとはいえません。  
なぜなら本来のDifyはノードとツールを合わせると100近いノードがあり、これらの情報を全て一つのPromptに入れることは難しいからです。  
もちろんGeminiのような2Mtokenにわたる情報をコンテキストに含めることが可能なLLMもありますが、精度が落ちていくためやはり難しいです。  

またLLMにDifyのDSLyamlが事前学習されるのであれば、プロンプトに入れる必要もなくなるのですが  
  
1. DSLの公式情報がDifyから出ていない  
2. Difyは中国企業なのでOpenAIやClaudeに事前学習されにくい  
  
というわけでDifyのDSLを事前学習したLLMは中国側から出てくることを祈るか自作するしかない状況です  
https://huggingface.co/models?search=dify  
現状(2025年1月3日現在)huggingface上にもDSLを事前学習したコード生成ものは見当たらず  
DeepSeekなど有名どころの中国系LLMにも学習されていませんでした  
そもそもDifyの開発速度が週に一度はリリースしたいと言ってるので、DSLを事前学習したLLMは毎週屑鉄になるので無しです。  

## 本プロジェクトのアプローチ

1. ユーザー入力から計画を立ててエッジ部分だけまずは生成
2. エッジ上から舐めていきノード一個ずつに分解してループする
3. LOOP内では SubTaskが ノード名からノードの情報を取得し出力
4. 4.で出力されたノードの情報から ノードのDSLを一つ分生成
5. 全てのエッジをなめるまで 2-4を繰り返す
6. 5で出力された一つ一つのノード.ymlと1で生成したエッジを統合して一つのDSL.yamlにする
7. 6の出力で失敗しやすいポイントを確認する先生を複数用意してダブルチェックさせる

## 本プロジェクトの問題点

ノード一つにつき1回APIを叩くのでAPI料金が高くなる。

## 問題点の解決方法

DeepSeek ならめっちゃやっすいいいい！！！！！！
と思っていましたが、DeepSeekのAPIが最近落ちるのでo3-miniにしました


# 環境
- Python3.12  
- langchain 0.3.14  

# 実行方法

`python main.py --user_request 'テキストを受け取り大阪弁に直して出力するワークフロー' --output_path dsl.yml`

## パラメータ
--user_request 生成したいワークフローの説明
--output_path 生成したDSLの出力先


## 現状できないこと


1. tool類は 変数名が  [](https://github.com/langgenius/dify/blob/8fbc9c9342bad65126772983cf634e19540149be/api/core/tools/entities/tool_entities.py#L100) text,json,image,blobと変幻自在になりますがtextで固定しています。

2. チャットBOTは作れません、ワークフローのみです

3. 以下にあるテストは通っていますが、5回同じPromptを投げて1回くらい失敗したWFを吐き出してしまいます。


## 実行可能なワークフローを作成できるPromptテスト

以下はOpenAIのo1に頼んで作ってもらったテストです。

---
- [x] 1. レベル1
「入力された内容をそのまま出力してください。」
解説: 最もシンプルに、受け取ったテキストを一切変えずにそのまま返すイメージです。

- [x] 2. レベル2
「入力文を、行数を変えずに全角スペースを半角スペースに置き換えて出力してください。」

解説: 文字列の変換やフォーマットだけを行う簡易的なワークフローを想定しています。

- [x] 3. レベル3
「与えられた文章の単語数を数えて、その数だけを返してください。」

解説: 入力された文章から情報を抽出し、単に数値として返すパターンです。

- [x] 4. レベル4
「入力された文章が敬体（です・ます調）で書かれているかどうかを判定し、“敬体です” もしくは “常体です” と返してください。」

解説: テキストのスタイルを判定するだけのシンプルな条件分岐をイメージしています。

- [x] 5. レベル5
「与えられた文章が質問かどうかを見分け、質問なら『これは質問です』と答え、そうでなければそのまま文章を返してください。」

解説: 入力がクエスチョンマーク等を含むかどうか、などで振り分けする例です。

- [x] 6. レベル6
「入力された文章を要約してください。なるべく短い要約を返してください。」

解説: 要約を行うワークフローです。自然言語要約をする際にLLMを利用するイメージを持っています。

- [] 7. レベル7
「質問が入力されたとき、社内のナレッジベースを検索し、見つかった情報を元に回答を生成してください。」

解説: 質問が来たら、内部または外部の知識ベースを使って回答する処理を想定しています。
→　ナレッジはIDの特定が必要なため難度が高いため後回し

- [x] 8. レベル8
「入力されたテキストをプログラミング言語のコードブロック形式に整形して返してください。」

解説: 入力文をMarkdown形式などのコードブロックに変換するだけの操作です。

- [x] 9. レベル9
「複数のキーワードが入力されたとき、キーワードごとに検索クエリを作成し、全検索結果を一つの文章にまとめて返してください。」

解説: リスト操作や外部検索を想定し、結果を一つのテキストに集約する流れのイメージです。

- [x] 10. レベル10
「数値を1つ入力すると、その数値の2乗と3乗を計算し、両方の値を返してください。」

解説: 数値を受け取り、簡単な数値演算を行って結果を返す例です。


- [x] 11. レベル11
「入力文から人名らしき単語をすべて抽出し、それらをコンマ区切りで返してください。」

解説: NLP的な処理で固有名詞（人名）を抽出するフローをイメージしています。

- [x] 12. レベル12
「ユーザーからの外部のAPIを叩いて天気情報を取得し、依頼文と天気情報をまとめて返してください。」

解説: 外部APIを呼び出して取得した結果を、元のテキストと合成して返す流れです。
→ 天気情報を取得するためのURLをどこから取得するか、またAPI_KEYをどうするか。
    →　今回は、URLとAPI_KEYをユーザーから指定する方法で通す
「ユーザーの入力した地方名や国名から、OpenWeatherMap API(https://api.openweathermap.org/data/2.5/weather?q={英語で地名 Ex.Tokyo}&appid=KKEEYY&units=metric&lang=ja)を使って天気情報を取得し、天気情報をいい感じにまとめて日本語にして返してください、API_KEYはstartで取得してください」



- [x] 13. レベル13
「ユーザーのレビューをカテゴリ分けし、カテゴリごとに別々のフォーマットで回答を生成してください。」

解説: まず文章を分類してから、分類結果ごとに異なる対応をするワークフローを想定しています。

- [x] 14. レベル14
「指示されたURLを読み込み、記事の主要な段落を抽出してまとめたサマリーを返してください。」

解説: WebページやPDFなどをテキスト化し、主要情報を抽出して要約するイメージです。

- [] 15. レベル15
「住所リストを入力し、1件ずつジオコーディングAPIで緯度経度を取得し、すべての結果をJSON形式で出力してください。」

解説: リストデータに対して繰り返し処理を行い、外部APIから取得した結果を一括してまとめる流れです。

- [] 16. レベル16
「ユーザーが送ったPDFファイルの内容をテキスト化し、その中に含まれる特定のキーフレーズの出現回数を返してください。」

解説: ドキュメント（PDF）をテキスト化して内容を解析し、数値情報を出力するケースを想定しています。

- [] 17. レベル17
「リスト形式のデータを受け取り、各要素を特定のルールで整形した上で、重複を除去し、ユニークな値だけを改行区切りで出力してください。」

解説: リスト操作をしながら、余分なものは除外する加工フローです。

- [] 18. レベル18
「ユーザーが行いたい操作を複数指定できるフォームを想定し、入力内容に応じて繰り返し処理を行い、それぞれの結果を最終的に結合して出力してください。」

解説: 繰り返し処理を開始する部分と、分岐を組み合わせ、最後に結果をまとめるイメージです。
→　ワークフロー自動作成では実現が難しい

- [] 19. レベル19
「問い合わせ内容に応じて、複数の外部ツールを呼び出して実行結果を集計し、ユーザーにわかりやすくサマライズしてください。」

解説: 目的に応じて複数ツールを呼び出し、すべての実行結果を統合した要約を返す流れをイメージしています。
→　複数ツールを特定しないと無理がある


- [] 20. レベル20
「ユーザーから与えられたコンテンツを、段階的に変換・加工して最終的に高品質なレポートを作成し、PDF出力可能な形で返してください。」

解説: 入力された多種多様な情報をもとに複雑な加工を行い、最終アウトプットを別のフォーマット（PDFのもとになる形）で生成する一連の流れを想定しています。

## ライセンス
本プロジェクトはMITライセンスです
