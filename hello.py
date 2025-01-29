import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st
import yaml
from matplotlib import font_manager as fm

FONT_PATH = os.path.join(os.getcwd(), "NOTO_SANS_JP/NotoSansJP-Regular.otf")
FONT_PROP = fm.FontProperties(fname=FONT_PATH)


def load_checklist():
    """チェックリストをYAMLファイルから読み込む"""
    with open("checklist.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["checklist"]


# Percentile 型のデータを作成
class Percentile:
    def __init__(self, color, result, percentile, name, start_date, sprint_duration):
        self.start_date = start_date
        self.color = color
        self.sprints = np.percentile(result, percentile)
        self.percentile = percentile
        self.name = name
        self.sprint_duration = sprint_duration

    def finish_date(self):
        return self.start_date + pd.DateOffset(days=self.sprints * self.sprint_duration)


def create_velocity_sampler(data):
    """
    Generate random samples for the true mean based on a t-distribution.

    Parameters:
    - data: list or array-like, the sample data
    - num_samples: int, number of random samples to generate (default: 1000)

    Returns:
    - random_samples: numpy array of sampled true means
    """

    data = np.array(data)
    mean = np.mean(data)
    # std = mean * 0.8
    # pre = np.random.normal(mean, std, 10)
    data = np.append([mean / 1.5, mean * 1.5], data)
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    sem = std / np.sqrt(n)
    df = n - 1
    t_dist = stats.t(df)

    def sampler(num_samples=1000):
        return mean + sem * t_dist.rvs(size=num_samples)

    return sampler


def guess_velocity_posterior(data):
    """
    Generate the posterior distribution of the true mean using Bayes' theorem.

    Parameters:
    - data: list or array-like, the observed sample data
    - prior_mean: float, the mean of the prior distribution
    - prior_std: float, the standard deviation of the prior distribution
    - num_samples: int, number of random samples to generate (default: 1000)

    Returns:
    - posterior_samples: numpy array of sampled posterior true means
    """

    data = np.array(data)
    n = len(data)
    prior_mean = np.mean(data)
    prior_std = prior_mean
    sample_mean = np.mean(data)
    sample_std = np.std(data, ddof=1)
    sem = sample_std / np.sqrt(n)

    # Update posterior parameters
    posterior_variance = 1 / (1 / prior_std**2 + n / sem**2)
    posterior_mean = posterior_variance * (
        prior_mean / prior_std**2 + n * sample_mean / sem**2
    )
    posterior_std = np.sqrt(posterior_variance)
    st.write(f"post mean: {posterior_mean:.2f}, Post std: {posterior_std:.2f}")

    def velocity_sampler(num_samples=1000):
        return np.random.normal(posterior_mean, posterior_std, num_samples)

    return velocity_sampler


def main():
    st.title("アジャイルプロジェクト予測")
    st.write("アジャイルチームのリリース時期をモンテカルロシミュレーションします。")

    # シミュレーションパラメータ
    st.header("ストーリーポイント")
    st.caption("リリースマイルストンまでの合計ストーリーポイントを入力してください。")
    story_point = st.slider(
        "合計ストーリーポイント", min_value=100, max_value=500, value=300, step=10
    )

    st.header("チーム")
    st.caption(
        "直近のベロシティをカンマ区切りで入力してください。入力件数が安定して増える毎にベロシティの安定度が上がるようにヒューリスティックを設定しています。"
    )
    velocities = st.text_input("直近のベロシティ", "50,55")
    try:
        velocity_list = [int(v) for v in velocities.split(",")]
        if len(velocity_list) < 1:
            st.error("ベロシティは1つ以上のデータが必要です。")
            return
        if any(v < 0 for v in velocity_list):
            st.error("ベロシティが負の値になっています。")
            return
    except ValueError:
        st.error("ベロシティはカンマ区切りの正の整数で入力してください。")
        return

    velocity_sampler = create_velocity_sampler(velocity_list)

    st.header("スコープクリープ")
    st.caption(
        "現在の合計ストーリーに潜在するリスクが大きい場合は大きい値を設定してください"
    )
    if not st.checkbox("リスクをチェックリストから判断する"):
        scope_creep_mean = st.number_input(
            "スコープクリープによる追加ストーリーの増加率 (%/sprint)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.5,
        )
        scope_creep_std_dev = scope_creep_mean
    else:
        st.caption(
            "スコープクリープの数値を推定するために、以下のチェックリストから該当する項目を選択してください。"
        )

        checklist = load_checklist()
        selected_checklist = []
        for item in checklist:
            if st.checkbox(item):
                selected_checklist.append(item)
        scope_creep_mean = 0
        scope_creep_std_dev = 0
        if selected_checklist:
            scope_creep_mean = len(selected_checklist) * 0.5
            scope_creep_std_dev = len(selected_checklist) * 0.5

    st.header("設定")
    # スプリント期間が何日か。
    sprint_duration_options = {
        "1週間": 7,
        "2週間": 14,
        "4週間": 28,
        "1ヶ月": 30,
        "2ヶ月": 60,
    }
    sprint_duration_label = st.selectbox(
        "スプリント期間", list(sprint_duration_options.keys()), index=1
    )
    sprint_duration = sprint_duration_options[sprint_duration_label]
    # 開始日はいつか。デフォルトは今日
    start_date = st.date_input(
        "開始日", value=pd.to_datetime("today"), min_value=None, max_value=None
    )
    # 終了したい日付を指定する
    end_date = st.date_input(
        "終了日（終了を予定している日付）",
        value=None,
        min_value=start_date + pd.DateOffset(days=1),
        max_value=start_date + pd.DateOffset(years=2),
    )

    num_simulations = st.number_input(
        "シミュレーション回数", min_value=2000, max_value=5000, value=3000, step=100
    )

    # 設定値の確認

    simulation_results = monte_carlo_simulation(
        story_point=story_point,
        velocity_sampler=velocity_sampler,
        scope_creep_mean=scope_creep_mean,
        scope_creep_std_dev=scope_creep_std_dev,
        num_simulations=num_simulations,
    )
    median = Percentile(
        "red", simulation_results, 50, "中央値", start_date, sprint_duration
    )
    commitment = Percentile(
        "green",
        simulation_results,
        60,
        "コミットメットライン",
        start_date,
        sprint_duration,
    )
    business_target = Percentile(
        "orange",
        simulation_results,
        80,
        "ビジネスターゲットライン",
        start_date,
        sprint_duration,
    )
    safety = Percentile(
        "blue", simulation_results, 90, "安全ライン", start_date, sprint_duration
    )

    deadlines = [median, commitment, business_target, safety]

    sprint_max = max(median.sprints * 3, safety.sprints * 1.1)
    sprint_min = 0

    # Plot histogram and smooth curve
    fig, ax = plt.subplots()
    ax.set_xlim(sprint_min, sprint_max)

    ax.hist(
        simulation_results,
        bins=500,
        range=(0, sprint_max),
        density=True,
        alpha=0.3,
        color="blue",
        edgecolor="white",
        label="見積り",
    )

    for perc in deadlines:
        ax.axvline(
            perc.sprints,
            color=perc.color,
            linestyle="-",
            linewidth=1.5,
            label=f"{perc.name} ({perc.sprints:.1f}スプリント)",
        )

    if end_date:
        diff_days = (end_date - start_date).days
        sprints = diff_days / sprint_duration
        # 何パーセントで終了するかを逆算する
        finish_rate = (
            np.searchsorted(np.sort(simulation_results), sprints)
            / len(simulation_results)
            * 100
        )
        ax.axvline(
            sprints,
            color="black",
            linestyle="--",
            linewidth=1.5,
            label=f"終了日予定 ({sprints:.1f}スプリント 終了確率{finish_rate:.1f}%)",
        )

    ax.set_title("完了スプリント数の確率分布", fontproperties=FONT_PROP)
    ax.set_xlabel("スプリント数", fontproperties=FONT_PROP)
    ax.set_ylabel("確率密度", fontproperties=FONT_PROP)
    ax.legend(
        facecolor="white",
        framealpha=1,
        loc="upper right",
        fontsize="small",
        prop=FONT_PROP
    )
    # Display plot in Streamlit
    st.pyplot(fig)

    # スプリント数を日付に変換
    median_date = median.finish_date()
    commitment_date = commitment.finish_date()
    business_target_date = business_target.finish_date()
    safety_date = safety.finish_date()

    # データを辞書として準備
    data = {
        "指標": [
            "中央値",
            "コミットメットライン(60%tile)",
            "ビジネスターゲットライン(80%tile)",
            "安全ライン(90%tile)",
        ],
        "スプリント数": [
            f"{median.sprints:.1f}",
            f"{commitment.sprints:.1f}",
            f"{business_target.sprints:.1f}",
            f"{safety.sprints:.1f}",
        ],
        "日付": [
            f"{median_date:%Y/%m/%d}",
            f"{commitment_date:%Y/%m/%d}",
            f"{business_target_date:%Y/%m/%d}",
            f"{safety_date:%Y/%m/%d}",
        ],
    }

    # データフレームを作成
    df = pd.DataFrame(data)

    # Streamlitでテーブル表示
    st.table(df.style.hide(axis="index"))


def monte_carlo_simulation(
    story_point: int,
    velocity_sampler: callable,
    scope_creep_mean: float,
    scope_creep_std_dev: float,
    num_simulations: int,
) -> np.ndarray:
    """
    Run Monte Carlo simulation to estimate the number of sprints needed.

    Args:
        num_tasks (int): Total number of tasks in the project.
        story_point_mean (float): Mean story points per task.
        story_point_std_dev (float): Standard deviation of story points.
        velocity_mean (float): Mean velocity of the team per sprint.
        velocity_std_dev (float): Standard deviation of velocity.
        scope_creep_mean (float): Mean percentage increase in tasks per sprint
            due to scope creep.
        scope_creep_std_dev (float): Standard deviation of scope creep.
        num_simulations (int): Number of Monte Carlo simulations to run.

    Returns:
        np.ndarray: Array of the number of sprints required for each simulation.
    """

    # Array to store results
    simulation_results = []

    for _ in range(num_simulations):
        total_tasks = float(story_point)
        velocity_per_sprint = max(0, velocity_sampler(1)[0])
        sprints = 0.0
        while total_tasks > 0:
            if sprints > 300:
                # Limit the number of sprints to prevent infinite loops
                # print("Exceeded 300 sprints, breaking loop.")
                break
            if total_tasks <= velocity_per_sprint:
                # Last sprint - calculate partial sprint
                sprints += total_tasks / velocity_per_sprint
                break
            else:
                sprints += 1
                creep_rate = np.random.normal(
                    1 + scope_creep_mean / 100, scope_creep_std_dev / 100
                )
                total_tasks = total_tasks * creep_rate
                total_tasks -= velocity_per_sprint

        simulation_results.append(sprints)

    return np.array(simulation_results)


if __name__ == "__main__":
    # サイドバーでツールを選択するためのセレクトボックス
    tool = st.sidebar.selectbox(
        "使用するツールを選択してください", ("アジャイルプロジェクト予測", "ツールB")
    )
    main()
