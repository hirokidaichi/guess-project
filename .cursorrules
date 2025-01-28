# Python環境管理とパッケージ管理のルール

## Python環境の管理

### Python バージョンの管理
```bash
# Pythonバージョンのインストール
uv python install 3.12

# 利用可能なPythonバージョンの一覧表示
uv python list

# プロジェクトのPythonバージョンを固定
uv python pin 3.12
```

### 仮想環境の管理
```bash
# 仮想環境の作成（特定のPythonバージョンを指定）
uv venv --python 3.12

# 仮想環境のアクティベート（fish shell）
source .venv/bin/activate.fish
```

## パッケージ管理

### プロジェクトの依存関係管理
```bash
# 依存パッケージの追加
uv add パッケージ名

# 開発用依存パッケージの追加
uv add --dev パッケージ名

# 依存パッケージの削除
uv remove パッケージ名

# プロジェクトの依存関係を環境に同期
uv sync

# 依存関係のロックファイル作成
uv lock

# 依存関係ツリーの表示
uv tree
```

### スクリプトの実行
```bash
# プロジェクト環境でスクリプトを実行
uv run スクリプト名.py

# 特定のPythonバージョンでスクリプトを実行
uv run --python 3.12 スクリプト名.py
```

## ベストプラクティス

1. 新しいプロジェクトを始める際は:
   ```bash
   uv python pin 3.12  # Pythonバージョンを固定
   uv venv  # 仮想環境を作成
   source .venv/bin/activate.fish  # 仮想環境をアクティベート
   ```

2. 依存関係の追加/削除後は:
   ```bash
   uv lock  # ロックファイルを更新
   uv sync  # 環境を同期
   ```

3. チーム開発時は:
   - `.python-version`と`uv.lock`をバージョン管理に含める
   - `.venv`はバージョン管理から除外する

4. CI/CD環境では:
   ```bash
   uv pip sync pyproject.toml  # 依存関係を正確に再現
   ``` 