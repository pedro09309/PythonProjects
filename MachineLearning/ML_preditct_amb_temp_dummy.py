import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def generate_temperature_data(n_samples=864, dt_seconds=150):
    np.random.seed(42)

    # Define the number of samples per phase
    samples_per_hour = 3600 // dt_seconds  # 24 samples/hour
    n_ramp_down = 4 * samples_per_hour     # 96 samples
    n_hold = 2 * samples_per_hour          # 48 samples
    n_ramp_up = n_samples - n_ramp_down - n_hold  # 720 samples

    # 1. Ramp down from 24°C to 12°C
    ramp_down = np.linspace(24, 12, n_ramp_down)

    # 2. Hold at 12°C
    hold = np.full(n_hold, 12.0)

    # 3. Ramp up from 12°C to 26°C
    ramp_up = np.linspace(12, 26, n_ramp_up)

    # Combine profile
    T_ambient = np.concatenate([ramp_down, hold, ramp_up])

    # Add small noise to ambient
    T_ambient += 0.3 * np.random.randn(n_samples)

    # Simulate biased internal sensor: offset + thermal inertia
    dynamic_bias = 1.5 + 0.5 * np.sin(np.linspace(0, 2 * np.pi, n_samples))
    T_internal = T_ambient + dynamic_bias + 0.2 * np.random.randn(n_samples)

    return T_internal.reshape(-1, 1), T_ambient

def run_temperature_regression():
    X, y = generate_temperature_data()
    time_steps = np.arange(len(X))

    X_train, X_test, y_train, y_test, t_train, t_test = train_test_split(
        X, y, time_steps, test_size=0.25, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\n--- Ambient Temperature Estimation Model ---\n")
    print(f"Test MSE: {mse:.4f}")
    print(f"Test RMSE: {np.sqrt(mse):.4f} °C")
    print(f"Test R²: {r2:.4f}")

    # Create 1 row, 2 columns subplot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Top plot: training data time series
    ax1.plot(X_train.flatten(), label="T_internal (biased)", color='orange', alpha=0.8)
    ax1.plot(y_train, label="T_ambient (true)", color='green', alpha=0.8)
    ax1.set_title("Training Data: Internal vs Ambient Temperature Over Time")
    # Custom x-axis ticks every 12h
    tick_every_12h = 288  # samples
    max_index = len(X_train)
    tick_positions = np.arange(0, max_index, tick_every_12h)
    tick_labels = [f"{int(x * 150 / 3600)}h" for x in tick_positions]  # convert to hours

    ax1.set_xticks(tick_positions)
    ax1.set_xticklabels(tick_labels)
    ax1.set_xlabel("Time (12h intervals)")
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_ylim(0, 30)
    ax1.legend()
    ax1.grid(True)

    # ⏱ Add 12-hour interval markers
    twelve_hour_samples = np.arange(0, len(X_train), 288)
    for x in twelve_hour_samples:
        ax1.axvline(x, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)

    # Bottom plot: test predictions
    ax2.scatter(X_test, y_test, color='blue', label='Test true values', alpha=0.5)
    ax2.scatter(X_test, y_pred, color='red', label='Test predictions', alpha=0.5)
    ax2.set_title("Test Data vs Model Predictions")
    ax2.set_xlabel("T_internal (°C)")
    ax2.set_ylabel("T_ambient (°C)")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_temperature_regression()
