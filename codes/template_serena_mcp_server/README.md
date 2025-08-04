# Serena MCP Server Docker Template

このテンプレートは、Serena Model Context Protocol (MCP) サーバーをDockerで実行するための設定ファイル一式です。

## 構成ファイル

- `docker-compose.override.yml` - Serena MCP サーバーのDocker Compose設定

## 使用方法

### 1. 環境変数の設定

`docker-compose.override.yml` で `PROJECT_PATH` 環境変数を設定してください：

```yaml
environment:
  - PROJECT_PATH=/app  # コンテナ内のプロジェクトパス
```

### 2. Docker Composeを使用して起動

```bash
# Docker Composeを使用して起動
docker-compose up -d

# ログを確認
docker-compose logs -f serena_mcp_server
```

### 3. サーバーの動作確認

Serena MCPサーバーは以下のポートで動作します：
- ポート 9121: MCP Server-Sent Events (SSE) エンドポイント

```bash
# サーバーの状態確認
curl http://localhost:9121
```

## Serena MCP Server について

このサーバーは [Serena](https://github.com/oraios/serena) を使用してModel Context Protocol (MCP) サーバーを提供します。

### 特徴

- **Docker化**: 設定済みのDockerコンテナで簡単に起動
- **SSEトランスポート**: Server-Sent Eventsを使用したリアルタイム通信
- **自動依存関係管理**: `uvx` を使用してSerenaを自動でインストール・実行
- **プロジェクト統合**: 指定されたプロジェクトパスでMCPサーバーを起動

## 設定

主要な設定項目：

- `PROJECT_PATH` - コンテナ内のプロジェクトパス
- `TZ=Asia/Tokyo` - タイムゾーン設定
- ポート `9121` - MCP SSEサーバーポート

`docker-compose.override.yml` を編集して設定をカスタマイズできます。

## MCP Serverの設定
```json
{
  "mcpServers": {
      "serena": {
        "type": "http",
        "url": "http://serena_mcp_server:9121/sse"
      }
  }
}


```
## トラブルシューティング

### コンテナが起動しない場合

```bash
# ログを確認
docker-compose logs serena_mcp_server

# コンテナの状態確認
docker-compose ps
```
