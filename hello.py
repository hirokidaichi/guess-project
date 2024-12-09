import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde



def main():
    st.title("Agile Project Management ")

    # シミュレーションパラメータ
    st.header("Task")
    num_tasks = st.slider("タスク数", min_value=10, max_value=500, value=100, step=10)
    story_point_mean = st.number_input("ストーリーポイントの平均値", min_value=1.0, max_value=20.0, value=10.0, step=0.5)
    story_point_std_dev = st.number_input("ストーリーポイントの標準偏差", min_value=0.1, max_value=10.0, value=2.0, step=0.1)

    st.header("Team")
    velocity_mean = st.number_input("ベロシティの平均値", min_value=50.0, max_value=200.0, value=100.0, step=10.0)
    velocity_std_dev = st.number_input("ベロシティの標準偏差", min_value=1.0, max_value=50.0, value=20.0, step=1.0)

    st.header("Scope Cleep")
    scope_creep_mean = st.number_input("スコープクリープの平均増加率 (%)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    scope_creep_std_dev = st.number_input("スコープクリープの標準偏差 (%)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)

    st.header("Settings")
    num_simulations = st.slider("シミュレーション回数", min_value=100, max_value=5000, value=2000, step=100)

    # 設定値の確認

    simulation_results = monte_carlo_simulation(
        num_tasks=num_tasks,
        story_point_mean=story_point_mean,
        story_point_std_dev=story_point_std_dev,
        velocity_mean=velocity_mean,
        velocity_std_dev=velocity_std_dev,
        scope_creep_mean=scope_creep_mean,
        scope_creep_std_dev=scope_creep_std_dev,
        num_simulations=num_simulations,
    )
    percentiles = np.percentile(simulation_results, [50, 60, 80, 90])
    colors = {
        50: "red",
        60: "yellow",
        80: "cyan",
        90: "green"
    }
    # Calculate range for x-axis
    mean = np.percentile(simulation_results, 50)
    max = int(mean*3)
    # Smooth distribution using KDE
    kde = gaussian_kde(simulation_results)
    kde_x = np.linspace(0, max, max*10)
    kde_y = kde(kde_x)

    # Plot histogram and smooth curve
    fig, ax = plt.subplots()
    ax.set_xlim(0, max)
    # ax.hist(simulation_results, bins=50, range=(0, 50), density=True, alpha=0.5, color='orange', edgecolor='black', label='Histogram')
    ax.plot(kde_x, kde_y, color='blue', label='Estimation', linewidth=2)
    for perc, value in zip([50, 60, 80, 90], percentiles):
        ax.axvline(value, color=colors[perc], linestyle="--", linewidth=1.5, label=f"{perc}%tile: {value:.1f}")

    ax.set_title("Monte Carlo Simulation: Histogram vs Smoothed Curve")
    ax.set_xlabel("Number of Sprints")
    ax.set_ylabel("Density")
    ax.legend()

    # Display plot in Streamlit
    st.pyplot(fig)


def monte_carlo_simulation(
    num_tasks: int,
    story_point_mean: float,
    story_point_std_dev: float,
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
    # Generate task durations based on normal distribution
    task_durations = np.random.normal(story_point_mean, story_point_std_dev, num_tasks)

    # Array to store results
    simulation_results = []

    # Run simulations
    for _ in range(num_simulations):
        total_tasks = np.sum(task_durations)
        velocity_per_sprint = np.random.normal(velocity_mean, velocity_std_dev)
        sprints = 0

        while total_tasks > 0:
            sprints += 1
            # Apply scope creep
            creep_rate = np.random.normal(scope_creep_mean / 100, scope_creep_std_dev / 100)
            total_tasks += total_tasks * creep_rate
            # Deduct velocity
            total_tasks -= velocity_per_sprint

        simulation_results.append(sprints)

    return np.array(simulation_results)




if __name__ == "__main__":
    main()
