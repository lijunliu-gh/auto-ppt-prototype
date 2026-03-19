# ユーザーガイド

このドキュメントは、開発者ではなく利用者向けです。

このプロジェクトが現在何をできるのか、どのような場面に向いているのか、どう操作すればよいのかを知りたい場合は、まずここを読んでください。

## これは何か

これは、AI エージェントから呼び出せる PowerPoint 生成バックエンドのプロトタイプです。

単なる PPT テンプレートスクリプトでもなく、完全な research agent でもありません。

実務上は次のように理解すると分かりやすいです。

- 上流の AI エージェントが要求理解、資料収集、調査、コンテキスト整理を行う
- このプロジェクトが入力を deck JSON に変換し、PowerPoint ファイルを出力する

つまり:

`requirements + source material -> deck JSON -> PPTX`

## 向いている場面

現時点では次のような用途に向いています。

- 製品戦略プレゼン
- 経営層向けレビュー資料
- 営業提案 deck
- プロジェクト振り返り deck
- 研修資料の初稿
- 公式サイト、PDF、DOCX、Markdown brief に基づくプレゼン生成
- 初稿を作ってから複数回改訂するワークフロー

## 今できること

### 1. 既存 JSON から直接 PPT を生成

すでに構造化された deck データがある場合に使います。

コマンド:

```bash
npm run generate
```

入力ファイル:

- `sample-input.json`

出力ファイル:

- `output/sample-deck.pptx`

### 2. 自然言語プロンプトから PPT を生成

大まかな要求だけがある場合に使います。

コマンド:

```bash
npm run generate:mock
```

モデル設定がある場合は次も使えます。

```bash
npm run generate:prompt
```

直接実行例:

```bash
node generate-from-prompt.js --prompt "Create an 8-slide AI product strategy deck for executives in a professional tone"
```

### 3. ソース資料付きで PPT を生成

現実の利用では、この方法が最も推奨されます。

要求文に加えて、次のような資料を渡せる場合に使います。

- 製品 brief
- 公式 URL
- PDF
- DOCX
- Markdown メモ

コマンド:

```bash
npm run generate:source
```

このスクリプトは次を読み込みます。

- `sample-source-brief.md`

自分の資料を渡すこともできます。

```bash
node generate-from-prompt.js --mock --prompt "Create an 8-slide strategy deck" --source your-brief.md --source https://example.com/product
```

### 4. 既存 deck を改訂

初稿を作成したあとで改善したい場合に使います。

典型的な改訂指示:

- スライド枚数を減らす
- もっと結論先行にする
- 実行計画を強調する
- 構成を組み直す
- 経営層向けに寄せる

コマンド:

```bash
npm run revise:mock
```

直接実行例:

```bash
node revise-deck.js --deck output/generated-deck.json --prompt "Compress this deck, make it more conclusion-driven, and emphasize the execution plan"
```

### 5. 別のエージェントから skill として使う

他のエージェントワークフローに組み込みたい場合に使います。

コマンド:

```bash
npm run skill:create
npm run skill:revise
```

関連ファイル:

- `agent-skill.js`
- `sample-agent-request.json`
- `sample-agent-revise-request.json`
- `skill-manifest.json`

### 6. HTTP サービスとして使う

ローカル API として統合したい場合に使います。

サービス起動:

```bash
npm run skill:server
```

ヘルスチェック:

```bash
curl http://localhost:3010/health
```

エンドポイント呼び出し:

```bash
curl -X POST http://localhost:3010/skill -H "Content-Type: application/json" --data @sample-http-request.json
```

## ソース資料の扱い

これは現在の製品で特に重要な部分です。

対応しているソース種別:

- ローカルテキストファイル: `txt`、`md`、`csv`、`json`、`yaml`、`xml`
- ローカル HTML
- ローカル PDF
- ローカル DOCX
- 画像ファイル参照
- HTTP / HTTPS URL

### 現在のソース表示方針

既定では:

- スライド本文にはソースを表示しない
- presenter notes にはソースを表示する
- スライドごとのソースは構造化メタデータにも保持する

つまり:

- 観客向けのスライドは見た目がすっきりしたまま
- 発表者は notes で根拠を確認できる
- revise や監査のときにもソースを再利用できる

## 推奨ワークフロー

比較的厳密なプレゼンを作るなら、プロンプトだけに頼らないでください。

より良い流れは次のとおりです。

1. プレゼンの目的を明確にする。
2. ソース資料を渡す。
3. 初稿を生成する。
4. 1 回から 3 回ほど改訂する。

例:

1. 目的を渡す。
   例: 経営層向けの 8 枚の製品戦略 deck。
2. 資料を渡す。
   例: 製品 brief、公式 URL、市場分析 PDF、社内メモ。
3. 初稿を生成する。
   `generate-from-prompt.js` を使う。
4. 改訂する。
   6 枚に圧縮する、結論先行にする、実行計画を強化する、投資家向けに組み替える。

## 最初に試す 3 つのコマンド

まず素早く試したいだけなら、次の順番がおすすめです。

### Step 1: source-aware generation を試す

```bash
npm run generate:source
```

### Step 2: skill mode を試す

```bash
npm run skill:create
```

### Step 3: revise mode を試す

```bash
npm run revise:mock
```

## 主なファイルの役割

### 利用者にとって特に重要なファイル

- `README.md`
  - 英語のメイン概要
- `PRODUCT.en.md`
  - 英語の製品概要とプロジェクトの位置付け
- `USER_GUIDE.zh-CN.md`
  - 簡体字中国語のユーザーガイド
- `sample-input.json`
  - サンプル deck 入力
- `sample-source-brief.md`
  - サンプルソース資料
- `sample-agent-request.json`
  - skill create 用サンプル request
- `sample-agent-revise-request.json`
  - skill revise 用サンプル request
- `sample-http-request.json`
  - HTTP 用サンプル request

### 技術統合向けの中心ファイル

- `generate-ppt.js`
  - deck JSON を PPT にレンダリングする
- `generate-from-prompt.js`
  - prompt から deck と PPT を生成する
- `revise-deck.js`
  - 既存 deck を改訂する
- `deck-agent-core.js`
  - planning、revise、schema validation の中核
- `source-loader.js`
  - ソース読み込みと抽出
- `agent-skill.js`
  - JSON skill エントリーポイント
- `skill-server.js`
  - HTTP skill エントリーポイント
- `deck-schema.json`
  - deck JSON 契約
- `skill-manifest.json`
  - skill integration 契約

## まだ弱い部分

このプロジェクトは完全なプロトタイプの流れを通せますが、まだ本番品質の製品ではありません。

現在の弱点は次のとおりです。

- 完全な research agent ではない
- OCR とマルチモーダル理解は未完成
- スライド単位のソース結び付けはまだ粗い
- ブランドテンプレートと見た目の制御はまだ基本的
- 複雑なケースでは上流モデルとエージェント品質への依存が大きい

## このプロジェクトの捉え方

最も適切な理解は、これを次のようなものとして見ることです。

- AI エージェント向けの PPT skill backend
- ソース資料を読める deck planning engine
- `.pptx` を出力する PowerPoint プロトタイプシステム

中核的な価値は、ローカル CLI のおもちゃであることではありません。

本当の価値は次の点です。

**より大きな AI エージェントワークフローから呼び出せる構造がすでに揃っていることです。**

## 一行まとめ

現時点でこのフォルダーは次の流れを実行できます。

- `prompt -> deck -> pptx`
- `prompt + sources -> deck -> pptx`
- `existing deck + revise prompt -> revised deck -> pptx`
- `agent request -> skill response`
- `HTTP request -> generated PPT artifacts`