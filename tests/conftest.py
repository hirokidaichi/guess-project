"""pytestの共通フィクスチャとヘルパー関数"""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_velocity_data():
    """テスト用のベロシティデータ"""
    return [10.0, 12.0, 11.0, 13.0, 9.0]  # 平均11.0


@pytest.fixture
def consistent_velocity_data():
    """一貫したベロシティデータ"""
    return [10.0, 10.1, 9.9, 10.0, 10.0]  # ほぼ10.0


@pytest.fixture
def small_velocity_data():
    """少数のベロシティデータ"""
    return [10.0, 11.0]


@pytest.fixture
def outlier_velocity_data():
    """外れ値を含むベロシティデータ"""
    return [10.0, 11.0, 12.0, 50.0]


@pytest.fixture
def sample_date():
    """テスト用の基準日"""
    return pd.Timestamp("2024-01-01")


def create_mock_velocity_sampler(fixed_velocity):
    """固定値を返すモックサンプラーを作成

    Args:
        fixed_velocity (float): 固定のベロシティ値

    Returns:
        callable: 指定された数のサンプルを生成する関数
    """

    def mock_sampler(num_samples):
        return np.full(num_samples, fixed_velocity)

    return mock_sampler
