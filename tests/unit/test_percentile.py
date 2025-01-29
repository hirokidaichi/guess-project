"""Percentileクラスのテスト"""

import numpy as np
import pandas as pd

from hello import Percentile


def test_percentile_initialization():
    """Percentileクラスの初期化テスト"""
    # テストデータ
    color = "red"
    result = np.array([1, 2, 3, 4, 5])
    percentile = 50
    name = "テスト"
    start_date = pd.Timestamp("2024-01-01")
    sprint_duration = 14

    # インスタンス化
    p = Percentile(
        color=color,
        result=result,
        percentile=percentile,
        name=name,
        start_date=start_date,
        sprint_duration=sprint_duration,
    )

    # 各属性の検証
    assert p.color == color
    assert p.percentile == percentile
    assert p.name == name
    assert p.start_date == start_date
    assert p.sprint_duration == sprint_duration
    assert p.sprints == np.percentile(result, percentile)


def test_finish_date_calculation():
    """finish_date()メソッドの計算テスト"""
    # テストデータ
    start_date = pd.Timestamp("2024-01-01")
    sprint_duration = 14
    result = np.array([2.0, 3.0, 4.0])  # 中央値は3.0スプリント

    p = Percentile(
        color="blue",
        result=result,
        percentile=50,
        name="テスト",
        start_date=start_date,
        sprint_duration=sprint_duration,
    )

    # 期待される終了日は開始日 + (スプリント数 * スプリント期間)
    expected_finish_date = start_date + pd.DateOffset(days=3.0 * sprint_duration)
    assert p.finish_date() == expected_finish_date


def test_finish_date_with_zero_sprints():
    """スプリント数が0の場合のfinish_date()テスト"""
    start_date = pd.Timestamp("2024-01-01")
    result = np.array([0.0, 0.0, 0.0])

    p = Percentile(
        color="red",
        result=result,
        percentile=50,
        name="テスト",
        start_date=start_date,
        sprint_duration=14,
    )

    # スプリント数が0の場合、開始日と同じ日付が返される
    assert p.finish_date() == start_date


def test_finish_date_with_fractional_sprints():
    """小数点のスプリント数の場合のfinish_date()テスト"""
    start_date = pd.Timestamp("2024-01-01")
    sprint_duration = 14
    result = np.array([1.5, 1.5, 1.5])  # 1.5スプリント

    p = Percentile(
        color="green",
        result=result,
        percentile=50,
        name="テスト",
        start_date=start_date,
        sprint_duration=sprint_duration,
    )

    # 1.5スプリントの場合、21日後（14日 * 1.5）になることを確認
    expected_finish_date = start_date + pd.DateOffset(days=1.5 * sprint_duration)
    assert p.finish_date() == expected_finish_date
