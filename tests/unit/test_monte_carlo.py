"""monte_carlo_simulation関数のテスト"""

import numpy as np
import pytest
from conftest import create_mock_velocity_sampler

from hello import monte_carlo_simulation


def test_monte_carlo_basic():
    """基本的なシミュレーション機能のテスト"""
    # 固定の速度（10ポイント/スプリント）を返すサンプラー
    velocity_sampler = create_mock_velocity_sampler(10.0)

    # シミュレーションパラメータ
    story_point = 100  # 合計100ポイント
    scope_creep_mean = 0.0  # スコープクリープなし
    scope_creep_std_dev = 0.0
    num_simulations = 1000

    # シミュレーション実行
    results = monte_carlo_simulation(
        story_point=story_point,
        velocity_sampler=velocity_sampler,
        scope_creep_mean=scope_creep_mean,
        scope_creep_std_dev=scope_creep_std_dev,
        num_simulations=num_simulations,
    )

    # 結果の検証
    assert len(results) == num_simulations
    assert np.all(results == 11.0)  # わざと間違った値に変更


def test_monte_carlo_with_scope_creep():
    """スコープクリープがある場合のテスト"""
    velocity_sampler = create_mock_velocity_sampler(10.0)

    # スコープクリープあり（確定的に5%/スプリント増加）
    results = monte_carlo_simulation(
        story_point=100,
        velocity_sampler=velocity_sampler,
        scope_creep_mean=5.0,
        scope_creep_std_dev=0.0,
        num_simulations=1000,
    )

    # スコープクリープがある場合、完了までのスプリント数は増加する
    assert np.all(results > 10.0)  # 基本ケース（10スプリント）より多くなる


def test_monte_carlo_zero_velocity():
    """速度が0の場合のテスト"""
    velocity_sampler = create_mock_velocity_sampler(0.0)

    results = monte_carlo_simulation(
        story_point=100,
        velocity_sampler=velocity_sampler,
        scope_creep_mean=0.0,
        scope_creep_std_dev=0.0,
        num_simulations=10,
    )

    # 速度が0の場合、無限ループを防ぐために300スプリントで打ち切られる
    assert np.all(results >= 300.0)


def test_monte_carlo_small_story():
    """小さなストーリーポイントの場合のテスト"""
    velocity_sampler = create_mock_velocity_sampler(10.0)

    results = monte_carlo_simulation(
        story_point=5,
        velocity_sampler=velocity_sampler,
        scope_creep_mean=0.0,
        scope_creep_std_dev=0.0,
        num_simulations=1000,
    )

    # 5ポイント ÷ 10ポイント/スプリント = 0.5スプリント
    assert np.all(results == 0.5)


def test_monte_carlo_negative_story():
    """負のストーリーポイントの場合のテスト"""
    velocity_sampler = create_mock_velocity_sampler(10.0)

    results = monte_carlo_simulation(
        story_point=-1,
        velocity_sampler=velocity_sampler,
        scope_creep_mean=0.0,
        scope_creep_std_dev=0.0,
        num_simulations=1000,
    )

    # 負のストーリーポイントの場合、0スプリントとして扱われる
    assert np.all(results == 0.0)


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
