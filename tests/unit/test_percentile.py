"""Percentileクラスのテスト"""

import numpy as np
import pandas as pd
import pytest

from hello import Percentile


@pytest.mark.parametrize(
    "color,data,percentile,name,start_date,sprint_duration,expected_sprints",
    [
        (
            "red",
            [10.0, 20.0, 30.0],
            50,
            "中央値",
            pd.Timestamp("2024-01-01"),
            14,
            20.0,
        ),
        (
            "blue",
            [5.0, 15.0, 25.0],
            90,
            "安全ライン",
            pd.Timestamp("2024-01-01"),
            7,
            15.0,
        ),
    ],
)
def test_percentile_initialization(
    color, data, percentile, name, start_date, sprint_duration, expected_sprints
):
    """Percentileクラスの初期化テスト"""
    data_array = np.array(data)
    perc = Percentile(color, data_array, percentile, name, start_date, sprint_duration)
    assert perc.color == color
    assert perc.name == name
    assert perc.start_date == start_date
    assert perc.sprint_duration == sprint_duration
    assert isinstance(perc.sprints, float)


def test_finish_date_calculation():
    """finish_dateメソッドの基本的な計算テスト"""
    start_date = pd.Timestamp("2024-01-01")
    sprint_duration = 14
    data = np.array([10.0])
    perc = Percentile("red", data, 50, "テスト", start_date, sprint_duration)
    perc.sprints = 10.0
    expected_date = start_date + pd.DateOffset(days=140)  # 10スプリント * 14日
    assert perc.finish_date() == expected_date


def test_finish_date_with_zero_sprints():
    """スプリント数が0の場合のfinish_dateテスト"""
    start_date = pd.Timestamp("2024-01-01")
    sprint_duration = 14
    data = np.array([0.0])
    perc = Percentile("red", data, 50, "テスト", start_date, sprint_duration)
    perc.sprints = 0.0
    assert perc.finish_date() == start_date


def test_finish_date_with_fractional_sprints():
    """小数点のスプリント数の場合のfinish_dateテスト"""
    start_date = pd.Timestamp("2024-01-01")
    sprint_duration = 7
    data = np.array([10.0])
    perc = Percentile("red", data, 50, "テスト", start_date, sprint_duration)
    perc.sprints = 1.5
    expected_date = start_date + pd.DateOffset(days=int(1.5 * 7))
    assert perc.finish_date() == expected_date
