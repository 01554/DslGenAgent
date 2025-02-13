[x] 1. レベル1
「入力された内容をそのまま出力してください。」
解説: 最もシンプルに、受け取ったテキストを一切変えずにそのまま返すイメージです。

[x] 2. レベル2
「入力文を、行数を変えずに全角スペースを半角スペースに置き換えて出力してください。」

解説: 文字列の変換やフォーマットだけを行う簡易的なワークフローを想定しています。

[x] 3. レベル3
「与えられた文章の単語数を数えて、その数だけを返してください。」

解説: 入力された文章から情報を抽出し、単に数値として返すパターンです。

[x] 4. レベル4
「入力された文章が敬体（です・ます調）で書かれているかどうかを判定し、“敬体です” もしくは “常体です” と返してください。」

解説: テキストのスタイルを判定するだけのシンプルな条件分岐をイメージしています。

[x] 5. レベル5
「与えられた文章が質問かどうかを見分け、質問なら『これは質問です』と答え、そうでなければそのまま文章を返してください。」

解説: 入力がクエスチョンマーク等を含むかどうか、などで振り分けする例です。

[x] 6. レベル6
「入力された文章を要約してください。なるべく短い要約を返してください。」

解説: 要約を行うワークフローです。自然言語要約をする際にLLMを利用するイメージを持っています。

[] 7. レベル7
「質問が入力されたとき、社内のナレッジベースを検索し、見つかった情報を元に回答を生成してください。」

解説: 質問が来たら、内部または外部の知識ベースを使って回答する処理を想定しています。

[x] 8. レベル8
「入力されたテキストをプログラミング言語のコードブロック形式に整形して返してください。」

解説: 入力文をMarkdown形式などのコードブロックに変換するだけの操作です。

[x] 9. レベル9
「複数のキーワードが入力されたとき、キーワードごとに検索クエリを作成し、全検索結果を一つの文章にまとめて返してください。」

解説: リスト操作や外部検索を想定し、結果を一つのテキストに集約する流れのイメージです。

[x] 10. レベル10
「数値を1つ入力すると、その数値の2乗と3乗を計算し、両方の値を返してください。」

解説: 数値を受け取り、簡単な数値演算を行って結果を返す例です。


[x] 11. レベル11
「入力文から人名らしき単語をすべて抽出し、それらをコンマ区切りで返してください。」

解説: NLP的な処理で固有名詞（人名）を抽出するフローをイメージしています。

[] 12. レベル12
「外部のAPI([東京天気](https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json))を叩いて天気情報を取得し、受け取った情報の名から23区の天気を探して出力してください。」

解説: 外部APIを呼び出して取得した結果を、元のテキストと合成して返す流れです。

[] 13. レベル13
「ユーザーの文章をカテゴリ分けし、カテゴリごとに別々のフォーマットで回答を生成してください。」

解説: まず文章を分類してから、分類結果ごとに異なる対応をするワークフローを想定しています。

[] 14. レベル14
「指示されたURLを読み込み、記事の主要な段落を抽出してまとめたサマリーを返してください。」

解説: WebページやPDFなどをテキスト化し、主要情報を抽出して要約するイメージです。

[] 15. レベル15
「住所リストを入力し、1件ずつジオコーディングAPIで緯度経度を取得し、すべての結果をJSON形式で出力してください。」

解説: リストデータに対して繰り返し処理を行い、外部APIから取得した結果を一括してまとめる流れです。

[] 16. レベル16
「ユーザーが送ったPDFファイルの内容をテキスト化し、その中に含まれる特定のキーフレーズの出現回数を返してください。」

解説: ドキュメント（PDF）をテキスト化して内容を解析し、数値情報を出力するケースを想定しています。

[] 17. レベル17
「リスト形式のデータを受け取り、各要素を特定のルールで整形した上で、重複を除去し、ユニークな値だけを改行区切りで出力してください。」

解説: リスト操作をしながら、余分なものは除外する加工フローです。

[] 18. レベル18
「ユーザーが行いたい操作を複数指定できるフォームを想定し、入力内容に応じて繰り返し処理を行い、それぞれの結果を最終的に結合して出力してください。」

解説: 繰り返し処理を開始する部分と、分岐を組み合わせ、最後に結果をまとめるイメージです。

[] 19. レベル19
「問い合わせ内容に応じて、複数の外部ツールを呼び出して実行結果を集計し、ユーザーにわかりやすくサマライズしてください。」

解説: 目的に応じて複数ツールを呼び出し、すべての実行結果を統合した要約を返す流れをイメージしています。

[] 20. レベル20
「ユーザーから与えられたコンテンツを、段階的に変換・加工して最終的に高品質なレポートを作成し、PDF出力可能な形で返してください。」

解説: 入力された多種多様な情報をもとに複雑な加工を行い、最終アウトプットを別のフォーマット（PDFのもとになる形）で生成する一連の流れを想定しています。