# 製品概要

## 現在の製品ポジション

Auto PPT Prototype は、AI エージェント向けのオープンソース PowerPoint 生成バックエンドです。

現在提供している機能:

- プロンプトからの deck planning
- 自然言語指示による deck revise
- JSON Schema による構造検証
- `.pptx` レンダリング
- エージェントから呼び出せる JSON request / response フロー
- ローカル HTTP skill エンドポイント

## これは何か

本質的には planning-and-rendering engine です。

次の役割を持つ AI エージェントの後段に置くことを想定しています。

- 要件収集
- 不足情報の確認
- 信頼できる資料の取得
- アップロード文書の読解
- スクリーンショットや画像の確認
- 各スライドに何を載せるべきかの判断

## これは何ではないか

これ自体は完全な research agent ではありません。

また、単純な「Web 検索からスライドを作るツール」として説明すべきでもありません。

厳密な用途では、システムは次を優先すべきです。

1. 公式ソース
2. ユーザーがアップロードした資料
3. 明示的なユーザー指示
4. Web 検索は最後の補助手段

## 現在の公開インターフェース

- CLI create
- CLI revise
- JSON request / response skill wrapper
- HTTP service wrapper

## 現在のプロダクトギャップ

- PDF、DOCX、HTML、CSV、表計算資料に対するより強い ingestion
- 画像とスクリーンショットの理解
- より細かな provenance tracking
- より強いテーマとテンプレート対応
- より良いレイアウト品質とタイポグラフィ制御
- 自動テスト
- ホスティング運用向けのハードニング

## 推奨されるオープンソースの説明

推奨 GitHub description:

> Open-source PowerPoint planning and rendering backend for AI agents working from trusted sources, uploaded materials, and explicit user requirements.