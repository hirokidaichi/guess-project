"""monte_carlo_simulation関数のテスト"""

import numpy as np
import pytest
from conftest import create_mock_velocity_sampler

from hello import monte_carlo_simulation


@pytest.mark.parametrize(
    "story_point, velocity, scope_creep_mean, scope_creep_std_dev, expected_sprints",
    [
        (100, 10.0, 0.0, 0.0, 10.0),  # 基本ケース
        (100, 10.0, 5.0, 0.0, pytest.approx(10.0, rel=0.5)),  # スコープクリープあり
        (100, 0.0, 0.0, 0.0, 301.0),  # 速度0
        (5, 10.0, 0.0, 0.0, 0.5),  # 小さなストーリー
        (-1, 10.0, 0.0, 0.0, 0.0),  # 負のストーリー
    ],
)
def test_monte_carlo_simulation(
    story_point, velocity, scope_creep_mean, scope_creep_std_dev, expected_sprints
):
    """パラメータ化されたモンテカルロシミュレーションのテスト"""
    velocity_sampler = create_mock_velocity_sampler(velocity)
    results = monte_carlo_simulation(
        story_point=story_point,
        velocity_sampler=velocity_sampler,
        scope_creep_mean=scope_creep_mean,
        scope_creep_std_dev=scope_creep_std_dev,
        num_simulations=1000,
    )
    assert len(results) == 1000
    assert np.all(results == expected_sprints)


def test_monte_carlo_invalid_sampler():
    """無効なサンプラーの場合のテスト"""
    with pytest.raises((ValueError, TypeError, AttributeError)):
        monte_carlo_simulation(
            story_point=100,
            velocity_sampler=None,
            scope_creep_mean=0.0,
            scope_creep_std_dev=0.0,
            num_simulations=1000,
        )
