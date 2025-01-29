# 未完了のテストタスク

## 1. テスト環境のセットアップ
- [x] テストの実行方法をREADME.mdに追記

## 2. テストデータの準備
- [x] テストケースのパラメータ化

## 3. テストの改善
- [x] xfailの解消
  - [x] test_velocity_posterior_empty_input
  - [x] test_velocity_sampler_empty_input
- [x] 警告（alert）の解消
  - [x] "Mean of empty slice"の警告
  - [x] "invalid value encountered in scalar divide"の警告
  - [x] "Degrees of freedom <= 0 for slice"の警告
  - [x] "Module src was never imported"の警告
  - [x] "No data was collected"の警告

## 関連タスク
- カバレッジの改善については [coverage.md](coverage.md) を参照
- CI/CD対応については [ci.md](ci.md) を参照

## 注意点
- テストの追加時にhello.pyの既存コードは最小限の変更に留める
- 各テストは独立して実行可能にする
- テストの可読性と保守性を重視する
- 必要に応じてモックを使用してテストを分離する 
