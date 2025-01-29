# ユニットテスト タスクリスト

## 1. テスト環境のセットアップ
- [x] pytestのインストールと設定
- [x] テストディレクトリ構造の作成
- [x] conftest.pyの作成（必要な場合）
- [ ] テストの実行方法をREADME.mdに追記

## 2. 単体テストの実装（優先順位順）
- [x] Percentileクラスのテスト
  - [x] インスタンス化のテスト
  - [x] finish_date()メソッドのテスト
- [x] create_velocity_sampler関数のテスト
  - [x] 正常系のテスト
  - [x] エッジケースのテスト
- [x] guess_velocity_posterior関数のテスト
  - [x] 正常系のテスト
  - [x] エッジケースのテスト
- [x] monte_carlo_simulation関数のテスト
  - [x] 基本的なシミュレーションのテスト
  - [x] 境界値のテスト
  - [x] エッジケースのテスト

## 3. テストデータの準備
- [x] モックデータの作成
- [x] テストフィクスチャの準備
- [ ] テストケースのパラメータ化

## 4. CI/CD対応
- [ ] GitHub Actionsでのテスト自動実行の設定
- [ ] テストカバレッジの計測と可視化

## 注意点
- テストの追加時にhello.pyの既存コードは最小限の変更に留める
- 各テストは独立して実行可能にする
- テストの可読性と保守性を重視する
- 必要に応じてモックを使用してテストを分離する

# 未完了のテストタスク

## 1. テスト環境のセットアップ
- [ ] テストの実行方法をREADME.mdに追記

## 2. テストデータの準備
- [ ] テストケースのパラメータ化

## 3. CI/CD対応
- [ ] GitHub Actionsでのテスト自動実行の設定
- [ ] テストカバレッジの計測と可視化

## 4. テストの改善
- [ ] xfailの解消
  - [ ] test_velocity_posterior_empty_input
  - [ ] test_velocity_sampler_empty_input
- [ ] 警告（alert）の解消
  - [ ] "Mean of empty slice"の警告
  - [ ] "invalid value encountered in scalar divide"の警告
  - [ ] "Degrees of freedom <= 0 for slice"の警告
  - [ ] "Module src was never imported"の警告
  - [ ] "No data was collected"の警告

## 注意点
- テストの追加時にhello.pyの既存コードは最小限の変更に留める
- 各テストは独立して実行可能にする
- テストの可読性と保守性を重視する
- 必要に応じてモックを使用してテストを分離する 
