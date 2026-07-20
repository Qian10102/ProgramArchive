import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet

# Set font to support international characters
plt.rcParams['font.family'] = 'Times New Roman'

def load_data(file_name):
    """
    Load data from CSV file with robust error handling
    Args:
        file_name (str): Path to the CSV file
    Returns:
        pd.DataFrame or None: Loaded data or None if loading fails
    """
    try:
        # Read CSV file
        data = pd.read_csv(file_name)
        # Ensure timestamp column is datetime
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        # Handle column names case-insensitively
        columns = [col.lower() for col in data.columns]
        required_columns = ['timestamp', 'power', 'signal_strength']
        # Validate required columns
        for col in required_columns:
            if col not in columns:
                raise ValueError(f"Missing required column: {col}")
        return data
    except FileNotFoundError:
        print(f"Error: File {file_name} not found")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File {file_name} is empty")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def forecast_trends(data, variable, periods=24):
    """
    Generate time series forecast using Prophet
    Args:
        data (pd.DataFrame): Input data
        variable (str): Variable to forecast
        periods (int): Number of future periods to predict
    Returns:
        pd.DataFrame: Forecast results
    """
    # Normalize variable name
    variable = variable.lower()
    if variable not in ['power', 'signal_strength']:
        raise ValueError("Variable must be 'power' or 'signal_strength'")
    # Prepare data for Prophet
    df = pd.DataFrame({
        "ds": data["timestamp"],
        "y": data[variable]
    })
    # Handle missing values
    df['y'] = df['y'].fillna(df['y'].median())
    # Configure Prophet model
    model = Prophet(
        changepoint_prior_scale=0.05,  # Adjust trend sensitivity
        daily_seasonality=True,
        weekly_seasonality=True
    )
    # Fit the model
    model.fit(df)
    # Generate future predictions
    future = model.make_future_dataframe(
        periods=periods,
        freq='h',
        include_history=False
    )
    # Predict
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]


def visualize_forecast_multi_style(forecast_data, variable, title="Forecast"):
    """
    Create multi-style visualization of forecast data as separate images
    Args:
        forecast_data (pd.DataFrame): Forecast data
        variable (str): Variable being forecasted
        title (str): Base title for visualization
    """
    # Prepare hour column for box plot
    forecast_data['hour'] = pd.to_datetime(forecast_data['ds']).dt.hour
    # 1. Original Line Plot
    plt.figure(figsize=(12, 6))
    plt.plot(forecast_data['ds'], forecast_data['yhat'], label='Predicted Value', color='blue')
    plt.fill_between(forecast_data['ds'], forecast_data['yhat_lower'], forecast_data['yhat_upper'], alpha=0.2, color='blue', label='Confidence Interval')
    plt.title(f'{variable} - Basic Line Forecast', fontsize=14)
    plt.xlabel('Time')
    plt.ylabel(f'{variable} Value')
    plt.legend()
    plt.tight_layout()
    plt.savefig('forecast_line_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    # 2. Area Chart
    plt.figure(figsize=(12, 6))
    plt.fill_between(forecast_data['ds'], forecast_data['yhat_lower'], forecast_data['yhat_upper'], alpha=0.5, color='green', label='Prediction Range')
    plt.plot(forecast_data['ds'], forecast_data['yhat'], color='red', linewidth=2)
    plt.title(f'{variable} - Area Prediction Chart', fontsize=14)
    plt.xlabel('Time')
    plt.ylabel(f'{variable} Value')
    plt.legend()
    plt.tight_layout()
    plt.savefig('forecast_area_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    # 3. Box Plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='yhat', data=forecast_data)
    plt.title(f'{variable} - Hourly Forecast Box Plot', fontsize=14)
    plt.xlabel('Hour')
    plt.ylabel(f'{variable} Value')
    plt.tight_layout()
    plt.savefig('forecast_box_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    # 4. Bar Chart
    plt.figure(figsize=(12, 6))
    plt.bar(forecast_data['ds'], forecast_data['yhat'], color='purple', alpha=0.7, yerr=(forecast_data['yhat_upper'] - forecast_data['yhat_lower']) / 2, capsize=5)
    plt.title(f'{variable} - Prediction Bar Chart', fontsize=14)
    plt.xlabel('Time')
    plt.ylabel(f'{variable} Value')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('forecast_bar_chart.png', dpi=300, bbox_inches='tight')
    plt.close()

def get_user_input():
    """
    Prompt user to select forecast variable
    Returns:
        str: Selected variable to forecast
    """
    while True:
        print("Select variable to forecast:")
        print("1. Power")
        print("2. Signal Strength")
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == '1':
            return 'power'
        elif choice == '2':
            return 'signal_strength'
        else:
            print("Invalid choice. Please try again.")

def main_forecast():
    """
    Main function to orchestrate forecast process
    """
    try:
        # Load data
        file_name = "../Prediction/sensor_data.csv"
        data = load_data(file_name)
        if data is None:
            print("Data loading failed. Exiting program.")
            return
        # Get user input for variable
        variable = get_user_input()
        # Generate forecast
        forecast = forecast_trends(data, variable, periods=24)
        forecast.to_csv("forecast_data.csv", index=False)
        print("24-hour forecast stored in 'forecast_data.csv'")
        # Visualize forecast
        visualize_forecast_multi_style(forecast, variable, title=f"{variable.capitalize()} 24-Hour Forecast")
        print("Multiview forecast chart generated as 'forecast_multiview.png'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main_forecast()