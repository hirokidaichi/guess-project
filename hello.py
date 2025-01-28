from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def setup_japanese_font() -> fm.FontProperties:
    """日本語フォントを設定します。"""
    try:
        fpath = Path.cwd() / 'NOTO_SANS_JP' / 'NotoSansJP-Regular.otf'
        if not fpath.exists():
            st.error(f'フォントファイルが見つかりません: {fpath}')
            return fm.FontProperties()
        return fm.FontProperties(fname=str(fpath))
    except Exception as e:
        st.error(f'フォント設定エラー: {e!s}')
        return fm.FontProperties()

# Percentile 型のデータを作成
class Percentile:
    def __init__(self, color, result, percentile, name,start_date,sprint_duration):
        self.start_date = start_date
        self.color = color
        self.sprints = np.percentile(result, percentile)
        self.percentile = percentile
        self.name = name
        self.sprint_duration = sprint_duration

    def finish_date(self ):
        return self.start_date + pd.DateOffset(days=self.sprints * self.sprint_duration)




def main():
    st.title("アジャイルプロジェクト予測")

    st.write("ベロシティとスコープクリープから終了時期をモンテカルロシミュレーションします")

    # シミュレーションパラメータ
    st.header("ストーリーポイント")
    story_point = st.slider("累計ストーリーポイント", min_value=100, max_value=500, value=200, step=10)

    st.header("チーム")
    velocity_mean = st.number_input("ベロシティの平均値", min_value=10.0, max_value=200.0, value=30.0, step=10.0)

    velocity_std_dev = st.number_input("ベロシティの標準偏差", min_value=1.0, max_value=50.0, value=10.0, step=1.0)

    st.header("スコープクリープ")
    st.markdown("スコープクリープとは、追加のストーリーポイントがスプリントごとにどれだけ増加するかを表します。")
    scope_creep_mean = st.number_input("スコープクリープによる追加ストーリーの増加率 (%/sprint)", min_value=0.0, max_value=5.0, value=2.0, step=1.0)
    scope_creep_std_dev = st.number_input("スコープクリープの標準偏差 (%/sprint)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)

    st.header("設定")
    # スプリント期間が何日か。
    sprint_duration = st.number_input("スプリント期間 (日)", min_value=1, max_value=50, value=14, step=1)   
    # 開始日はいつか。デフォルトは今日
    start_date = st.date_input("開始日", value=pd.to_datetime('today'), min_value=None, max_value=None)
    # 終了したい日付を指定する
    end_date = st.date_input("終了日（終了を予定している日付）", 
        value=None, 
        min_value=start_date+pd.DateOffset(days=1), 
        max_value=start_date+pd.DateOffset(years=2))

    num_simulations = st.number_input("シミュレーション回数", min_value=2000, max_value=5000, value=3000, step=100)

    # 設定値の確認

    simulation_results = monte_carlo_simulation(
        story_point=story_point,
        velocity_mean=velocity_mean,
        velocity_std_dev=velocity_std_dev,
        scope_creep_mean=scope_creep_mean,
        scope_creep_std_dev=scope_creep_std_dev,
        num_simulations=num_simulations,
    )
    median = Percentile("red", simulation_results, 50, "中央値",start_date, sprint_duration)
    commitment = Percentile("green", simulation_results, 60, "コミットメットライン",start_date, sprint_duration)
    business_target = Percentile("orange", simulation_results, 80, "ビジネスターゲットライン",start_date, sprint_duration)
    safety = Percentile("blue", simulation_results, 90, "安全ライン",start_date, sprint_duration)

    deadlines = [median, commitment, business_target, safety]

    sprint_max = max(int(median.sprints)* 3,safety.sprints * 1.1)

    # Plot histogram and smooth curve
    fig, ax = plt.subplots()
    font_prop = setup_japanese_font()
    
    ax.set_xlim(0, sprint_max)
    ax.hist(simulation_results, bins=500, range=(0, sprint_max), density=True, alpha=0.3, color='blue', edgecolor='white', label='見積り')

    for perc in deadlines:
        ax.axvline(perc.sprints, color=perc.color, linestyle="-", linewidth=1.5, label=f"{perc.name} ({perc.sprints:.1f}スプリント)")   
    
    if end_date:
        diff_days = (end_date - start_date).days
        sprints = diff_days / sprint_duration
        # 何パーセントで終了するかを逆算する
        finish_rate = np.searchsorted(np.sort(simulation_results), sprints) / len(simulation_results) * 100
        ax.axvline(sprints, color="black", linestyle="--", linewidth=1.5, label=f"終了日予定 ({sprints:.1f}スプリント 終了確率{finish_rate:.1f}%)")
    
    ax.set_title("プロジェクト終了シミュレーション", fontproperties=font_prop)
    ax.set_xlabel("スプリント数", fontproperties=font_prop)
    ax.set_ylabel("確率密度", fontproperties=font_prop)
    ax.legend(facecolor='white', framealpha=1, prop=font_prop)

    # Display plot in Streamlit
    st.pyplot(fig)



    # スプリント数を日付に変換
    median_date = median.finish_date()
    commitment_date = commitment.finish_date()
    business_target_date = business_target.finish_date()
    safety_date = safety.finish_date()


    # データを辞書として準備
    data = {
        "指標": ["中央値", "コミットメットライン(60%tile)", "ビジネスターゲットライン(80%tile)", "安全ライン(90%tile)"],
        "スプリント数": [f"{median.sprints:.1f}", f"{commitment.sprints:.1f}", f"{business_target.sprints:.1f}", f"{safety.sprints:.1f}"],
        "日付": [f"{median_date:%Y/%m/%d}", f"{commitment_date:%Y/%m/%d}", f"{business_target_date:%Y/%m/%d}", f"{safety_date:%Y/%m/%d}"],
    }

    # データフレームを作成
    df = pd.DataFrame(data)

    # Streamlitでテーブル表示
    st.table(df.style.hide(axis='index'))
    

def monte_carlo_simulation(
    story_point: int,
    velocity_mean: float,
    velocity_std_dev: float,
    scope_creep_mean: float,
    scope_creep_std_dev: float,
    num_simulations: int
) -> np.ndarray:
    """
    Run Monte Carlo simulation to estimate the number of sprints needed.

    Args:
        num_tasks (int): Total number of tasks in the project.
        story_point_mean (float): Mean story points per task.
        story_point_std_dev (float): Standard deviation of story points.
        velocity_mean (float): Mean velocity of the team per sprint.
        velocity_std_dev (float): Standard deviation of velocity.
        scope_creep_mean (float): Mean percentage increase in tasks per sprint due to scope creep.
        scope_creep_std_dev (float): Standard deviation of scope creep.
        num_simulations (int): Number of Monte Carlo simulations to run.

    Returns:
        np.ndarray: Array of the number of sprints required for each simulation.
    """

    # Array to store results
    simulation_results = []

    # Run simulations
    for _ in range(num_simulations):
        total_tasks = float(story_point)
        velocity_per_sprint = max(0, np.random.normal(velocity_mean, velocity_std_dev))
        sprints = 0

        while total_tasks > 0:
            if sprints > 200:
                # Limit the number of sprints to prevent infinite loops
                break
            if total_tasks <= velocity_per_sprint:
                # Last sprint - calculate partial sprint
                sprints += total_tasks / velocity_per_sprint
                break
            else:
                sprints += 1
                # Apply scope creep
                creep_rate = np.random.normal(scope_creep_mean / 100, scope_creep_std_dev / 100)
                total_tasks += total_tasks * creep_rate
                # Deduct velocity
                total_tasks -= velocity_per_sprint

        simulation_results.append(sprints)

    return np.array(simulation_results)




if __name__ == "__main__":
    # サイドバーでツールを選択するためのセレクトボックス
    tool = st.sidebar.selectbox(
        "使用するツールを選択してください",
        ("アジャイルプロジェクト予測", "ツールB")
    )
    main()
