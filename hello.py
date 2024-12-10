import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_fontja # noqa 日本語フォント設定




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
    percentiles = np.percentile(simulation_results, [50, 60, 80, 90])
    percentiles_names = {
        50: {"color": "red", "name": "中央値"},
        60: {"color": "orange", "name": "コミットメットライン(60%tile)"},
        80: {"color": "blue", "name": "ビジネスターゲットライン(80%tile)"},
        90: {"color": "green", "name": "安全ライン(90%tile)"}
    }
    # Calculate range for x-axis
    mean = np.percentile(simulation_results, 50)
    max = int(mean*3)

    # Plot histogram and smooth curve
    fig, ax = plt.subplots()
    ax.set_xlim(0, max)
    ax.hist(simulation_results, bins=500, range=(0, max), density=True, alpha=0.3, color='blue', edgecolor='white', label='見積り')

    for perc, value in zip([50, 60, 80, 90], percentiles):
        ax.axvline(value, color=percentiles_names[perc]["color"], linestyle="-", linewidth=1.5, label=f"{percentiles_names[perc]['name']}")

    ax.set_title("プロジェクト終了シミュレーション")
    ax.set_xlabel("スプリント数")
    ax.set_ylabel("確率密度")
    ax.legend(facecolor='white', framealpha=1)

    # Display plot in Streamlit
    st.pyplot(fig)

    
    median = finish_date(start_date,np.percentile(simulation_results, 50), sprint_duration)
    commitment = finish_date(start_date,np.percentile(simulation_results, 60), sprint_duration)
    business_target = finish_date(start_date,np.percentile(simulation_results, 80), sprint_duration)
    safety = finish_date(start_date,np.percentile(simulation_results, 90), sprint_duration)
    

    # データを辞書として準備
    data = {
        "指標": ["中央値", "コミットメットライン(60%tile)", "ビジネスターゲットライン(80%tile)", "安全ライン(90%tile)"],
        "日付": [f"{median:%Y/%m/%d}", f"{commitment:%Y/%m/%d}", f"{business_target:%Y/%m/%d}", f"{safety:%Y/%m/%d}"]
    }

    # データフレームを作成
    df = pd.DataFrame(data)

    # Streamlitでテーブル表示
    st.table(df.style.hide(axis='index'))
    

def finish_date(start_date, sprint_duration, number_of_sprints):
    return start_date + pd.DateOffset(days=(sprint_duration * number_of_sprints))

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
