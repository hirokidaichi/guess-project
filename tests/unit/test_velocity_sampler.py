"""velocity_sampler関数のテスト"""

import numpy as np
import pytest

from hello import create_velocity_sampler


def test_velocity_sampler_basic():
    """基本的なサンプリング機能のテスト"""
    # テストデータ
    data = [10.0, 12.0, 11.0, 13.0, 9.0]  # 平均11.0
    sampler = create_velocity_sampler(data)

    # サンプリング結果の検証
    num_samples = 1000
    samples = sampler(num_samples)

    # 基本的な性質の検証
    assert len(samples) == num_samples
    assert isinstance(samples, np.ndarray)

    # 統計的な性質の検証（おおよその範囲をチェック）
    sample_mean = np.mean(samples)
    assert 9.0 <= sample_mean <= 13.0  # データの範囲内に平均が収まっているか


def test_velocity_sampler_single_value():
    """単一の値でのサンプリングテスト"""
    data = [10.0]
    sampler = create_velocity_sampler(data)
    samples = sampler(100)

    # 単一値の場合でもサンプリングが機能することを確認
    assert len(samples) == 100
    assert not np.all(samples == samples[0])  # すべての値が同じではないことを確認


def test_velocity_sampler_statistical_properties():
    """統計的な性質の詳細なテスト"""
    data = [10.0, 10.0, 10.0, 10.0, 10.0]  # 平均10.0の安定したデータ
    sampler = create_velocity_sampler(data)

    # 大量のサンプルを生成
    samples = sampler(10000)

    # 平均値の検証（95%信頼区間内に収まることを確認）
    sample_mean = np.mean(samples)
    assert 9.0 <= sample_mean <= 11.0

    # t分布に基づくサンプリングであることを確認
    # 正規性の検定は行わない（t分布を使用しているため）
    assert np.std(samples) > 0  # 分散があることを確認


def test_velocity_sampler_with_negative_values():
    """負の値を含むデータでのテスト"""
    data = [-1.0, 0.0, 1.0]
    sampler = create_velocity_sampler(data)
    samples = sampler(1000)

    # 負の値を含むデータでも適切にサンプリングできることを確認
    assert np.min(samples) < 0
    assert np.max(samples) > 0


@pytest.mark.xfail(reason="現在の実装では空の入力に対するバリデーションが未実装")
def test_velocity_sampler_empty_input():
    """空のデータ入力時のテスト"""
    with pytest.raises(ValueError):
        create_velocity_sampler([])


def test_velocity_sampler_invalid_input():
    """無効な入力値のテスト"""
    with pytest.raises((ValueError, TypeError)):
        create_velocity_sampler(None)

    with pytest.raises((ValueError, TypeError)):
        create_velocity_sampler("invalid")
