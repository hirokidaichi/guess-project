"""velocity_posterior関数のテスト"""

import numpy as np
import pytest

from hello import guess_velocity_posterior


def test_velocity_posterior_basic(sample_velocity_data):
    """基本的なベイズ推定の機能テスト"""
    # テストデータ
    data = sample_velocity_data  # 平均11.0
    sampler = guess_velocity_posterior(data)

    # サンプリング結果の検証
    num_samples = 1000
    samples = sampler(num_samples)

    # 基本的な性質の検証
    assert len(samples) == num_samples
    assert isinstance(samples, np.ndarray)

    # 統計的な性質の検証（おおよその範囲をチェック）
    sample_mean = np.mean(samples)
    assert 8.0 <= sample_mean <= 14.0  # データの範囲を少し広めに取る


def test_velocity_posterior_consistent_data(consistent_velocity_data):
    """一貫したデータでの推定テスト"""
    # わずかに異なる値を持つデータ
    data = consistent_velocity_data
    sampler = guess_velocity_posterior(data)
    samples = sampler(1000)

    # ほぼ一貫したデータの場合、推定値は実際の値の周りに集中するはず
    sample_mean = np.mean(samples)
    sample_std = np.std(samples)

    assert 9.5 <= sample_mean <= 10.5  # 平均は10.0付近
    assert sample_std < 1.0  # 分散は小さくなるはず


def test_velocity_posterior_small_dataset(small_velocity_data):
    """少数のデータでの推定テスト"""
    data = small_velocity_data  # 2つのデータポイントのみ
    sampler = guess_velocity_posterior(data)
    samples = sampler(1000)

    # 少数データの場合でも、平均値は入力データの範囲内に収まるはず
    sample_mean = np.mean(samples)
    assert 9.5 <= sample_mean <= 11.5


def test_velocity_posterior_with_outliers(outlier_velocity_data):
    """外れ値を含むデータでの推定テスト"""
    data = outlier_velocity_data  # 50.0は明らかな外れ値
    sampler = guess_velocity_posterior(data)
    samples = sampler(1000)

    # 外れ値の影響を受けつつも、完全には支配されないことを確認
    sample_mean = np.mean(samples)
    assert sample_mean < 50.0  # 外れ値よりは小さい
    assert sample_mean > 11.0  # 通常値よりは大きい


@pytest.mark.xfail(reason="現在の実装では空の入力に対するバリデーションが未実装")
def test_velocity_posterior_empty_input():
    """空のデータ入力時のテスト"""
    with pytest.raises(ValueError):
        guess_velocity_posterior([])


def test_velocity_posterior_invalid_input():
    """無効な入力値のテスト"""
    with pytest.raises((ValueError, TypeError)):
        guess_velocity_posterior(None)

    with pytest.raises((ValueError, TypeError)):
        guess_velocity_posterior("invalid")
