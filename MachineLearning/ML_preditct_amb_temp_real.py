import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score

def load_real_temperature_data():
    df = pd.read_csv('./MachineLearning/data/measurements.csv')

    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
    df_sorted = df.sort_values(by='publishedAt')
    timestamps = df["publishedAt"].values

    df_sorted['rawAmbientTemperature'] = pd.to_numeric(df_sorted['rawAmbientTemperature'], errors='coerce')
    T_internal = df_sorted['rawAmbientTemperature'].dropna().astype(float).values

    df_sorted['ambientTemperature'] = pd.to_numeric(df_sorted['ambientTemperature'], errors='coerce')
    T_ambient = df_sorted['ambientTemperature'].dropna().astype(float).values
    #T_ambient = T_internal - 5.0  # external temperature with fixed offset

    # Ensure all arrays have the same length
    min_length = min(len(T_internal), len(T_ambient), len(timestamps))
    T_internal = T_internal[:min_length]
    T_ambient = T_ambient[:min_length]
    timestamps = timestamps[:min_length]

    return T_internal.reshape(-1, 1), T_ambient, timestamps #reshape -> scikit-learn requires 2D arrays for X

def run_temperature_regression():
    X, y, timestamps = load_real_temperature_data()

    time_steps = np.arange(len(X))

    X_train, X_test, y_train, y_test, t_train, t_test = train_test_split(
        X, y, time_steps, test_size=0.25, random_state=42
    )

    # Result: Test MSE: 1.1404 | Test RMSE: 1.0679 °C | Test R²: 0.4885
    # model = LinearRegression()

    # Result: Test MSE: 0.9905 | Test RMSE: 0.9952 °C | Test R²: 0.5558
    # model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Result: Test MSE: 1.1656 | Test RMSE: 1.0796 °C | Test R²: 0.4772
    # model = DecisionTreeRegressor()

    # Result: Test MSE:  0.8389 | Test RMSE: 0.9159 °C | Test R²: 0.6237
    model = SVR()

    # Result: Test MSE: 0.9231 | Test RMSE: 0.9608 °C | Test R²: 0.5860
    # model = KNeighborsRegressor(n_neighbors=5)

    # Result: Test MSE: 1.1407 | Test RMSE: 1.0680 °C | Test R²: 0.4884
    # model = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=1000)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\n--- Ambient Temperature Estimation Model (Real Data) ---\n")
    # MSE = Mean Squared Error
    # It measures the average of the squared differences between predicted and actual values
    # Lower is better — 0 means perfect predictions.
    print(f"Test MSE: {mse:.4f}")

    # RMSE = Root Mean Squared Error
    # It's the square root of the MSE, giving the error in the same units as the target variable (in this case, degrees Celsius)
    # Easier to interpret because it tells you how far off your predictions are on average in °C
    print(f"Test RMSE: {np.sqrt(mse):.4f} °C")

    # R² = Coefficient of Determination
    # Tells how well the model explains the variance in the data.
    # Range: 0 to 1 (or negative if the model is worse than simply predicting the mean)
    # 1.0 = perfect fit, 0.0 = no better than mean, < 0 = worse than mean prediction
    print(f"Test R²: {r2:.4f}")

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Define time axis in hours (150s = 2.5 minutes = 0.04167 hours per sample)
    sampling_interval_sec = 150
    sampling_interval_hours = sampling_interval_sec / 3600  # 0.04167 hours

    time_axis_hours = np.arange(len(X)) * sampling_interval_hours

    # Top plot: time series with regular time axis
    ax1.plot(time_axis_hours, X.flatten(), label="T_internal (measured)", color='orange', alpha=0.8)
    ax1.plot(time_axis_hours, y, label="T_ambient (inferred)", color='green', alpha=0.8)
    ax1.set_title("Time Series: Internal vs Ambient Temperature")
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_xlabel("Time (hours)")
    ax1.set_ylim(0, max(X_train.max(), y_train.max()) + 2)
    ax1.legend()
    ax1.grid(True)

    # Set x-axis ticks every 12 hours
    tick_interval_hours = 12
    max_hours = time_axis_hours[-1]
    xticks = np.arange(0, max_hours + tick_interval_hours, tick_interval_hours)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels([f"{int(h)}h" for h in xticks])

    # Bottom plot: prediction accuracy
    ax2.scatter(X_test, y_test, color='blue', label='True values', alpha=0.5)
    ax2.scatter(X_test, y_pred, color='red', label='Predictions', alpha=0.5)
    ax2.set_title("Test Data vs Model Predictions")
    ax2.set_xlabel("T_internal (°C)")
    ax2.set_ylabel("T_ambient (°C)")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_temperature_regression()
