# Guess Project

プロジェクトの見積もりをモンテカルロシミュレーションで行うツール

## インストール

```bash
# Pythonバージョンの固定
uv python pin 3.12

# 仮想環境の作成
uv venv

# 仮想環境のアクティベート（fish shell）
source .venv/bin/activate.fish

# 依存パッケージのインストール
uv pip sync
```

## テスト

### テストの実行

基本的なテストの実行:
```bash
python -m pytest
```

詳細なテスト結果の表示:
```bash
python -m pytest -v
```

特定のテストファイルの実行:
```bash
python -m pytest tests/unit/test_monte_carlo.py
```

特定のテスト関数の実行:
```bash
python -m pytest tests/unit/test_monte_carlo.py::test_monte_carlo_basic
```

### テストカバレッジの確認

カバレッジレポートの生成:
```bash
python -m pytest --cov=src tests/
```

HTMLレポートの生成:
```bash
python -m pytest --cov=src --cov-report=html tests/
```
