# 統合ガイド

このドキュメントは、統合担当者向けです。

このプロジェクトを自分の AI エージェント、ワークフローエンジン、スクリプト、バックエンドサービス、またはローカルツールチェーンに組み込みたい場合は、このファイルを重点的に読んでください。

## 統合チェーンにおけるこのプロジェクトの役割

このプロジェクトは次のような役割に最も適しています。

- PPT generation backend
- deck planning and rendering engine
- local skill service
- agent-callable PPT workflow

完全な research agent を置き換えるものではありません。代わりに、上流から渡された入力を次の成果物に変換します。

- deck JSON
- `.pptx`

推奨される利用モデルは次のとおりです。

1. 上流エージェントがユーザー要求と資料を収集する。
2. 上流エージェントがこのプロジェクトを呼び出す。
3. このプロジェクトが deck JSON と PPTX を返す。
4. ユーザーが修正を求めたら、上流エージェントが revise フローを再度呼ぶ。

## 現在サポートされている統合方式

## 1. CLI 統合

最も簡単な方法です。次のようなケースに向いています。

- Claude Code 系ツール
- ローカル自動化スクリプト
- shell / PowerShell ワークフロー
- CI でのコマンド実行

### Create

```bash
node generate-from-prompt.js --prompt "Create an 8-slide product strategy deck"
```

### Create with sources

```bash
node generate-from-prompt.js --mock --prompt "Create an 8-slide product strategy deck" --source sample-source-brief.md
```

### Revise

```bash
node revise-deck.js --deck output/generated-deck.json --prompt "Compress this deck to 6 slides"
```

### Agent skill request mode

```bash
node agent-skill.js --request sample-agent-request.json --response output/agent-response.json
```

## 2. JSON Skill 統合

これは現在、エージェントワークフローに最も適した方法の一つです。

必要なのは次の 3 ステップだけです。

1. request JSON を書く
2. `agent-skill.js` を呼ぶ
3. response JSON を読む

### Create request 形式

```json
{
  "action": "create",
  "prompt": "Create an 8-slide AI agent product strategy deck for executives in a professional tone",
  "mock": true,
  "research": false,
  "contextFiles": [],
  "sources": [
    {
      "path": "sample-source-brief.md",
      "type": "text",
      "label": "Sample product brief",
      "trustLevel": "user-provided",
      "priority": "high"
    }
  ],
  "outputJson": "output/agent-generated-deck.json",
  "outputPptx": "output/agent-generated-deck.pptx"
}
```

### Revise request 形式

```json
{
  "action": "revise",
  "prompt": "Compress this deck, make it more conclusion-driven, and emphasize the execution plan",
  "mock": true,
  "research": false,
  "deckPath": "output/generated-deck.json",
  "contextFiles": [],
  "sources": [
    {
      "path": "sample-source-brief.md",
      "type": "text",
      "label": "Sample product brief",
      "trustLevel": "user-provided",
      "priority": "high"
    }
  ],
  "outputJson": "output/agent-revised-deck.json",
  "outputPptx": "output/agent-revised-deck.pptx"
}
```

### 呼び出し例

```bash
node agent-skill.js --request sample-agent-request.json --response output/agent-response.json
```

### Response 形式

```json
{
  "ok": true,
  "action": "create",
  "prompt": "string",
  "deckJsonPath": "absolute path",
  "pptxPath": "absolute path",
  "slideCount": 8,
  "assumptions": [],
  "sourcesUsed": []
}
```

## 3. HTTP 統合

上流システムが API 呼び出しを好む場合、このプロジェクトはローカル HTTP サービスとしても使えます。

### サービス起動

```bash
npm run skill:server
```

### ヘルスチェック

```bash
curl http://localhost:3010/health
```

### skill 呼び出し

```bash
curl -X POST http://localhost:3010/skill -H "Content-Type: application/json" --data @sample-http-request.json
```

### HTTP request body 例

```json
{
  "action": "create",
  "prompt": "Create an 8-slide AI agent product strategy deck for executives in a professional tone",
  "mock": true,
  "research": false,
  "contextFiles": [],
  "sources": [
    {
      "path": "sample-source-brief.md",
      "type": "text",
      "label": "Sample product brief",
      "trustLevel": "user-provided",
      "priority": "high"
    }
  ]
}
```

### HTTP ルート

- `GET /health`
- `POST /skill`

## 入力項目の説明

## 1. `prompt`

役割:

- プレゼンの目的を定義する
- 対象読者、トーン、枚数、用途を説明する

推奨される書き方:

- 目的が明確
- 対象が明確
- トーンが明確
- 枚数が明確

例:

```text
Create an 8-slide strategy deck for executives. Keep it concise, decision-oriented, and focused on execution priorities.
```

## 2. `contextFiles`

役割:

- 追加のコンテキスト資料を渡す
- テキストメモ、補足要件、内部コメントに向いている

型:

- ファイルパス配列

## 3. `sources`

役割:

- 信頼できる資料を渡す
- planning 前にコンテキストへ変換する
- スライド単位のソースメタデータを保持する
- 既定で presenter notes にソースを書き出す

対応ソース種別:

- text
- json
- html
- pdf
- docx
- image
- url

推奨される優先順位:

1. ユーザーがアップロードした資料
2. 公式製品ページ
3. 公式ドキュメント
4. 投資家向け資料
5. その他の外部情報源

## 4. `mock`

役割:

- ローカル mock planner を使うかどうかを決める

向いている用途:

- オフラインテスト
- ローカル統合作業
- モデルを呼ばずに経路だけ素早く検証したい場合

## 5. `research`

役割:

- 軽量な research 補助を有効にする

現在の注意点:

- Tavily が設定されている場合のみ動作する
- デモには便利だが、厳密な本番ワークフローでの最終的な事実根拠とはみなすべきではない

## deck 出力に含まれるもの

生成された deck JSON には現在次が含まれます。

- `sourceDisplayMode`
- `slides[].sources`
- `slides[].speakerNotes`

### 既定動作

現在の既定値:

- `sourceDisplayMode = notes`

これは次を意味します。

- ソースはスライド本文には表示されない
- ソースは presenter notes に表示される
- ソースは構造化メタデータにも保持される

## 推奨される統合モデル

AI エージェントに統合するなら、最も安定した流れは次のとおりです。

1. エージェントがユーザー目標を収集する
2. エージェントが信頼できる資料を集める
3. エージェントが request JSON を組み立てる
4. `agent-skill.js` を呼ぶ
5. response JSON を読む
6. 生成結果をユーザーに返す
7. 必要に応じて revise を再度呼ぶ

要するに、これは次のようなものとして扱うべきです。

- local skill
- local deck backend
- agent tool

完全に独立した最終ユーザー製品として扱うより、この位置付けの方が適切です。

## 統合先ごとの推奨

## Claude Code や coding-agent 系ツール向け

最適な方法:

- CLI 呼び出し
- または JSON request と `agent-skill.js`

理由:

- 単純
- ローカルパスの扱いが分かりやすい
- 複数回の revise を組み込みやすい

## サービス型システム向け

最適な方法:

- HTTP 呼び出し

理由:

- 既存バックエンドと統合しやすい
- 外部 workflow engine と接続しやすい

## ローカル自動化スクリプト向け

最適な方法:

- CLI モード

理由:

- デバッグが簡単
- 追加のサーバーライフサイクル管理が不要

## 現在の境界と注意点

## 1. 完全な research agent ではない

次のすべてを単独で実行できるとは考えないでください。

- 公式サイトの発見
- 複数ソースの比較
- 証拠の矛盾解消
- マルチモーダル解析

これらは上流エージェントの責務です。

## 2. 画像は現在「参照」であり、真の視覚理解ではない

画像はソースパイプラインには入れられますが、このリポジトリ自身が完全な OCR や画像推論を行うわけではありません。

## 3. スライド単位ソースはあるが、attribution はまだ粗い

deck 出力にはすでに次が含まれます。

- `slides[].sources`

ただし、まだ次までは対応していません。

- 特定の bullet がどの source fragment に対応するか
- 特定の chart 点がどのデータ断片に対応するか

## 4. レイアウトとブランド制御はまだプロトタイプ段階

企業向けの高度なテンプレート制御が必要なら、まだ追加実装が必要です。

## 重要ファイル

- `agent-skill.js`: JSON skill エントリーポイント
- `skill-server.js`: HTTP サービスエントリーポイント
- `skill-manifest.json`: skill 契約
- `generate-from-prompt.js`: create CLI
- `revise-deck.js`: revise CLI
- `source-loader.js`: ソース読み込み層
- `deck-agent-core.js`: planning 中核
- `generate-ppt.js`: PPT レンダラー
- `deck-schema.json`: deck schema 契約

## 一行アドバイス

今すぐ統合するなら、最も安定した道は次です。

**まず JSON skill モードで接続し、サービス型統合が必要になった時点で HTTP モードに上げることです。**