# DevContainer Template

汎用的な開発環境を提供するDevContainerテンプレートです。

## ディレクトリ構造

```
template_devcontainer/
├── .devcontainer/
│   ├── devcontainer.json      # DevContainer設定ファイル
│   └── setup-script.sh        # 初期化スクリプト
└── README.md                   # このドキュメント
```

## 含まれる機能

### ベースイメージ
- **Ubuntu Noble（24.04）**: `mcr.microsoft.com/devcontainers/base:noble`

### 環境設定
- **タイムゾーン**: Asia/Tokyo（日本時間）
- **コンテナ名**: `devcontainer-name`
- **ユーザー**: `vscode`
- **永続ボリューム**: ホームディレクトリ（`/home/vscode`）

### インストール済みFeatures
- **Git**: バージョン管理システム
- **Docker (outside-of-docker)**: コンテナ内からホストのDockerを使用可能
- **curl (apt-get版)**: HTTPクライアント

### VS Code拡張機能
- **GitHub Copilot**: AI支援コーディング（オプション）
- **GitHub Copilot Chat**: AI支援チャット（オプション）

## 使用方法

### 1. テンプレートのコピー
```bash
# プロジェクトディレクトリに移動
cd your-project/

# .devcontainerフォルダをコピー
cp -r path/to/template_devcontainer/.devcontainer .
```

### 2. VS Codeでの起動
1. VS Codeでプロジェクトを開く
2. 「Dev Containers: Rebuild Container」コマンドを実行
3. コンテナ作成時に`setup-script.sh`が自動実行される

## 自動セットアップについて

`postCreateCommand`により、コンテナ初回作成時に以下が自動実行されます：
```bash
bash ./.devcontainer/setup-script.sh
```

このスクリプトは：
- システムパッケージの更新
- エイリアスの設定（重複チェック付き）
- 設定状況のログ出力

## カスタマイズ例

### ポートフォワーディングの追加
```json
"forwardPorts": [3000, 8000, 8080]
```

### 環境変数の追加
```json
"containerEnv": {
    "TZ": "Asia/Tokyo",
    "ENVIRONMENT": "development",
    "DEBUG": "true"
}
```

### 追加の拡張機能
```json
"extensions": [
    "GitHub.copilot",
    "GitHub.copilot-chat",
    "ms-python.python",
    "ms-python.black-formatter",
    "bradlc.vscode-tailwindcss"
]
```

### setup-script.shの拡張
```bash
# 追加のパッケージインストール
sudo apt-get -y install nodejs npm postgresql-client

# Python環境のセットアップ
pip install --upgrade pip
pip install black isort pytest
```

## 注意事項

- エイリアス設定は重複チェック機能があるため、複数回実行しても安全です
- タイムゾーンは日本時間（Asia/Tokyo）に設定されています
- 永続ボリュームを使用しているため、ホームディレクトリの内容は保持されます
