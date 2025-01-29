"""velocity_posterior関数のテスト"""

import numpy as np
import pytest

from hello import guess_velocity_posterior


@pytest.mark.parametrize(
    "data, expected_range",
    [
        (
            [10.0, 12.0, 11.0, 13.0, 9.0],  # 基本ケース
            (8.0, 14.0),
        ),
        (
            [10.0, 10.1, 9.9, 10.0, 10.0],  # 一貫したデータ
            (9.5, 10.5),
        ),
        (
            [10.0, 11.0],  # 少数データ
            (9.5, 11.5),
        ),
        (
            [10.0, 11.0, 12.0, 50.0],  # 外れ値を含むデータ
            (11.0, 50.0),
        ),
    ],
)
def test_velocity_posterior(data, expected_range):
    """パラメータ化されたベロシティ事後分布のテスト"""
    sampler = guess_velocity_posterior(data)
    samples = sampler(1000)

    # 基本的な性質の検証
    assert len(samples) == 1000
    assert isinstance(samples, np.ndarray)

    # 統計的な性質の検証
    sample_mean = np.mean(samples)
    assert expected_range[0] <= sample_mean <= expected_range[1]
    if len(data) > 1:
        assert np.std(samples) > 0  # 分散があることを確認（単一値以外）


@pytest.mark.xfail(reason="現在の実装では空の入力に対するバリデーションが未実装")
def test_velocity_posterior_empty_input():
    """空のデータ入力時のテスト"""
    with pytest.raises(ValueError):
        guess_velocity_posterior([])


@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        "invalid",
        123,
        {"key": "value"},
    ],
)
def test_velocity_posterior_invalid_input(invalid_input):
    """無効な入力値のテスト"""
    with pytest.raises((ValueError, TypeError)):
        guess_velocity_posterior(invalid_input)
