import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score

def load_real_temperature_data():
    # df = pd.read_csv('./MachineLearning/data/measurements_2days.csv')
    # df = pd.read_csv('./MachineLearning/data/measurements_14days.csv')
    df = pd.read_csv('./MachineLearning/data/measurements_56days.csv')

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

    # Result: Error (RMSE): 1.00 °C | Accuracy(R²): 60.62 %
    # model = LinearRegression()

    # Result: Error (RMSE): 0.94 °C | Accuracy(R²): 65.28 %
    model = SVR()

    # Result: Error (RMSE): 1.00 °C | Accuracy(R²): 60.85 %
    # model = KNeighborsRegressor(n_neighbors=5)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\n--- Ambient Temperature Estimation Model (Real Data) ---\n")
    # RMSE = Root Mean Squared Error
    # It's the square root of the MSE, giving the error in the same units as the target variable (in this case, degrees Celsius)
    # Easier to interpret because it tells you how far off your predictions are on average in °C
    print(f"Error (RMSE): {np.sqrt(mse):.2f} °C")

    # R² = Coefficient of Determination
    # Tells how well the model explains the variance in the data.
    # Range: 0 to 1 (or negative if the model is worse than simply predicting the mean)
    # 1.0 = perfect fit, 0.0 = no better than mean, < 0 = worse than mean prediction
    print(f"Accuracy (R²): {r2 * 100:.2f} %")

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
    ax1.set_ylim(10, 40)
    ax1.legend()
    ax1.grid(True)

    # Set x-axis ticks every 168 hours
    tick_interval_hours = 168
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
    ax2.set_ylim(10, 40)
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_temperature_regression()
