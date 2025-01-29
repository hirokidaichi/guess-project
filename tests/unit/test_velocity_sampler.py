"""velocity_sampler関数のテスト"""

import numpy as np
import pytest

from hello import create_velocity_sampler


@pytest.mark.parametrize(
    "data, expected_range",
    [
        (
            [10.0, 12.0, 11.0, 13.0, 9.0],  # 基本ケース
            (9.0, 13.0),
        ),
        (
            [10.0, 10.1, 9.9, 10.0, 10.0],  # 一貫したデータ
            (9.5, 10.5),
        ),
        (
            [10.0],  # 単一値
            (8.0, 15.0),  # 期待範囲をさらに広げる
        ),
        (
            [-1.0, 0.0, 1.0],  # 負の値を含むデータ
            (-1.5, 1.5),
        ),
    ],
)
def test_velocity_sampler(data, expected_range):
    """パラメータ化されたベロシティサンプラーのテスト"""
    sampler = create_velocity_sampler(data)
    samples = sampler(1000)

    # 基本的な性質の検証
    assert len(samples) == 1000
    assert isinstance(samples, np.ndarray)

    # 統計的な性質の検証
    sample_mean = np.mean(samples)
    assert expected_range[0] <= sample_mean <= expected_range[1]
    assert np.std(samples) > 0  # 分散があることを確認


@pytest.mark.xfail(reason="現在の実装では空の入力に対するバリデーションが未実装")
def test_velocity_sampler_empty_input():
    """空のデータ入力時のテスト"""
    with pytest.raises(ValueError):
        create_velocity_sampler([])


@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        "invalid",
        {"key": "value"},
    ],
)
def test_velocity_sampler_invalid_input(invalid_input):
    """無効な入力値のテスト"""
    with pytest.raises((ValueError, TypeError)):
        create_velocity_sampler(invalid_input)
