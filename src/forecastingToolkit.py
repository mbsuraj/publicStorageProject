import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


def get_mape(y_true, y_pred):
    """
    Calculate the Mean Absolute Percentage Error (MAPE).

    Parameters:
        - y_true: Array-like, true values.
        - y_pred: Array-like, predicted values.

    Returns:
        - MAPE: Mean Absolute Percentage Error.
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


# Function to perform time series cross-validation
def time_series_cross_validation(model, time_series, n_splits):
    # Determine the fold size
    fold_size = len(time_series) // n_splits

    # Initialize a list to store RMSE values
    rmse_values = []
    # mape_values = []
    # Perform cross-validation
    for i in range(1, n_splits):
        start_idx = time_series.index[i * fold_size]
        end_idx = time_series.index[(i + 1) * fold_size]

        # Split the data into train and test sets using datetime-based indexing
        train_data = time_series.loc[time_series.index < start_idx]
        test_data = time_series.loc[(time_series.index >= start_idx) & (time_series.index < end_idx)]

        # Train the model on the training data
        if len(train_data) > 0:
            # Train the model on the training data
            results = model.fit(train_data)
        else:
            print(f"Train data is empty for fold {i}. Check your data or cross-validation setup.")
            continue

        # Make predictions on the test data
        predicted_values = results.forecast(steps=len(test_data))
        # Calculate RMSE for this fold
        rmse = np.sqrt(mean_squared_error(test_data, predicted_values))
        # mape = get_mape(test_data, predicted_values)

        rmse_values.append(rmse)
        # mape_values.append(mape)
    return rmse_values

def prepare_property_data(state):
    property_data = pd.read_csv("input_data/property locations.csv")
    property_data.CompletionDate = pd.to_datetime(property_data.CompletionDate, format='%Y-%m-%d')
    property_data["Week"] = property_data.CompletionDate.apply(lambda x: x.week)
    property_data["Year"] = property_data.CompletionDate.apply(lambda x: x.year)
    property_data["Month"] = property_data.CompletionDate.apply(lambda x: x.month)
    property_data['quarter'] = property_data.CompletionDate.apply(lambda x: x.quarter)
    # Extract the year, quarter, and the first month of the quarter
    property_data['year_quarter'] = property_data['CompletionDate'].dt.strftime('%Y-%m-01')
    # Adjust the month for the first month of the quarter
    property_data['year_quarter'] = property_data['year_quarter'].str[:5] + (
                (property_data['CompletionDate'].dt.quarter - 1) * 3 + 1).astype(str).str.zfill(2) + property_data[
                                                                                                         'year_quarter'].str[
                                                                                                     7:]
    property_data['year_month'] = property_data['CompletionDate'].dt.to_period('M').dt.to_timestamp(
        how="e").dt.strftime('%Y-%m-%d')
    # filter for completed properties only
    property_data = property_data[property_data["PropertyStatus"] == "Completed"]

    # filter only for california
    if state == "United States":
        pass
    else:
        property_data = property_data[property_data["State"] == state]

    # filter out data prior to completion date of 1972 and after 2023
    lower_limit = pd.to_datetime("1970-01-01")
    upper_limit = pd.to_datetime("2023-11-01")
    property_data = property_data[
        (property_data["CompletionDate"] > lower_limit) & (property_data["CompletionDate"] < upper_limit)]
    return property_data

def remove_outliers(property_data, col):
    Q1 = property_data[col].quantile(0.25)
    Q3 = property_data[col].quantile(0.75)
    IQR = Q3 - Q1

    # Define the upper and lower bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # ignore lower bounds
    property_data = property_data[(property_data[col] >= lower_bound) & (property_data[col] <= upper_bound)]
    return property_data

def get_rentable_sqft_by_month(property_data):
    # get rentable sqft by completion date
    property_data = property_data.sort_values(by=["CompletionDate"], ascending=True)
    rentable_sqft_added_ts = property_data[["NetRentableSqFt", "year_month"]].groupby(["year_month"]).sum()
    rentable_sqft_added_ts.index = pd.to_datetime(rentable_sqft_added_ts.index, format="%Y-%m-%d")

    # convert to Series object
    rentable_sqft_added_ts = rentable_sqft_added_ts["NetRentableSqFt"]
    rentable_sqft_added_ts = rentable_sqft_added_ts.asfreq("M")

    # Get the minimum and maximum dates from the existing DataFrame
    min_date = rentable_sqft_added_ts.index.min()
    max_date = pd.Timestamp('2023-10-31')  # Set the end date to October 2023
    # Create a new DataFrame with a date range from min_date to max_date
    date_range = pd.date_range(start=min_date, end=max_date, freq='M')
    # Create a DataFrame with zero values for 'year_month' and a new column, e.g., 'value'
    zero_data = pd.DataFrame({'year_month': date_range, 'value': 0})
    # Merge the new DataFrame with the existing one and fill missing values with zeros
    rentable_sqft_added_ts = pd.merge(zero_data, rentable_sqft_added_ts, on='year_month', how='left').fillna(0)

    rentable_sqft_added_ts.set_index("year_month", inplace=True)
    rentable_sqft_added_ts = rentable_sqft_added_ts["NetRentableSqFt"]
    return rentable_sqft_added_ts