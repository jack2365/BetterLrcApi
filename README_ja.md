# BetterLrcApi

[English](README.md) | [中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Русский](README_ru.md)

**BetterLrcApi** は、[HisAtri/LrcApi](https://github.com/HisAtri/LrcApi) プロジェクトをベースにリファクタリングおよびアップグレードされたバージョンです。元のプロジェクトのコア哲学を維持しながら、アルバムアートの品質とパフォーマンスを大幅に最適化しました。

オープンソースへの貢献について、原作者の [HisAtri](https://github.com/HisAtri) 氏に特別に感謝します。

## ✨ 主な特徴

*   **高解像度カバー (New)**: **Apple Music (iTunes Search API)** と統合し、最大 **3000x3000** 解像度の公式アルバムアートを提供します。これにより、カバーがぼやけたり一致しない問題が完全に解決されます。
*   **マルチソース歌詞**:
    *   **Netease (網易雲音楽)**: デフォルトのソース、高精度 (クラウド展開の場合は Cookie 設定を推奨)。
    *   **Kugou (酷狗音楽)**: 自動フォールバックソース (PC/アプリのデュアルインターフェースフォールバックをサポート)。
    *   **QQ Music (QQ音楽)**: **新規** 第3のフォールバックソース、Cookie 不要、高い可用性を確保。
*   **高性能アーキテクチャ**: Flask から **FastAPI** に移行し、非同期 (Async/Await) 並行処理を完全にサポートすることで、応答速度が大幅に向上しました。

## 🚀 クイックスタート

### Docker デプロイ (推奨)

> サポートされているアーキテクチャ: `linux/amd64`, `linux/arm64`

```bash
# イメージのプル
docker pull steelydk/betterlrcapi:latest

# コンテナの起動 (認証なし)
docker run -d \
  -p 8080:8080 \
  --name betterlrcapi \
  steelydk/betterlrcapi:latest
  
# コンテナの起動 (認証あり - 推奨)
docker run -d \
  -p 8080:8080 \
  --name betterlrcapi \
  -e API_AUTH="your_secret_key" \
  steelydk/betterlrcapi:latest
```

### 認証と設定

#### 1. API 認証 (API_AUTH)
API の乱用を防ぐため、`API_AUTH` 環境変数を設定できます。
*   起動時に `-e API_AUTH=your_secret_key` を追加します。
*   リクエスト時にヘッダーに `Authorization: your_secret_key` を追加します。

#### 2. Netease Cookie (NETEASE_COOKIE)
**クラウドサーバー (GitHub Codespaces, VPS) にデプロイした際に歌詞が 404 エラーになる場合**、通常は IP が Netease によって制限されているためです。
*   **解決策**: `NETEASE_COOKIE` 環境変数を設定します。
*   **取得方法**: ブラウザで網易雲音楽にログインし、F12 コンソールを開いて `document.cookie` と入力し、コピーします。
*   **例**:
    ```bash
    docker run -d ... -e NETEASE_COOKIE="MUSIC_U=..." ...
    ```

### ソースコードから実行 (Python)

1.  このプロジェクトをクローンまたはダウンロードします。
2.  依存関係をインストールします:
    ```bash
    pip install -r requirements.txt
    ```
3.  サービスを起動します:
    ```bash
    # 認証なし
    python3 -m uvicorn main:app --host 0.0.0.0 --port 8080
    
    # 認証あり
    API_AUTH=your_secret_key python3 -m uvicorn main:app --host 0.0.0.0 --port 8080
    ```

## 📚 API ドキュメント

### 1. カバー取得 `/cover`

Apple Music から高品質のアルバムアートを取得します。

*   **URL**: `/cover`
*   **メソッド**: `GET` または `POST`
*   **パラメータ**:
    *   `keyword`: 曲名とアーティスト名 (推奨)
    *   `title` + `artist`: 曲名とアーティスト名 (互換モード、検索用に自動的に結合されます)
    *   `format`: `redirect` (デフォルト、画像にリダイレクト) または `json` (JSON データを返す)

**例**:
```bash
# 方法 1: キーワード検索 (推奨)
GET /cover?keyword=Thinking Out Loud

# 方法 2: 分割パラメータ (Audio Station などと互換性あり)
GET /cover?title=Thinking Out Loud&artist=Ed Sheeran
```

### 2. 歌詞取得 `/lyrics`

LRC 形式の歌詞を取得します。

*   **URL**: `/lyrics`
*   **メソッド**: `GET` または `POST`
*   **パラメータ**:
    *   `keyword`: 曲名とアーティスト名
    *   `title` + `artist`: 曲名とアーティスト名 (互換モード)
    *   `format`: `text` (デフォルト、プレーンテキストを返す) または `json`

**例**:
```bash
# 方法 1: キーワード
GET /lyrics?keyword=Thinking Out Loud

# 方法 2: 分割パラメータ
GET /lyrics?title=Thinking Out Loud&artist=Ed Sheeran
```

### 📱 互換性

以下のアプリ API フォーマットに完全に適合しています:
*   **Format 1**: `<url>?title=<title>&artist=<artist>`
*   **Format 2**: `<url>/<artist>/<title>` (アプリがパラメータを自動変換)
*   **Synology Audio Station**: デフォルトの POST リクエストメソッドをネイティブサポート。

## 📝 開発と貢献

このプロジェクトは GPL-3.0 ライセンスの下でライセンスされています。Issue や PR の提出を歓迎します。

*   Original Author: [HisAtri](https://github.com/HisAtri)
*   BetterLrcApi Developer: [steely/Antigravity]
