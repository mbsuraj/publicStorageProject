import requests
import json
import pandas as pd
import time

# Define the BLS API key (you need to obtain your own API key)
api_key = "1b73b60dc8be4ec2ad240c873f8d7e62"
CENSUS_API_KEY = "bf4d5f56be5746c3e4a1f93df1aa2bd6549c27d1"

def get_unemployment_rate(start_year, end_year):
    # Define the BLS API endpoint and series ID for the unemployment rate
    api_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    series_id = "LNS14000000"  # Unemployment Rate: All Industries, Seasonally Adjusted

    # Initialize an empty DataFrame (set to None initially)
    df = None

    # Define the batch size (20 years in this case)
    batch_size = 20

    # Iterate through years in batches
    for batch_start in range(start_year, end_year, batch_size):
        batch_end = min(batch_start + batch_size - 1, end_year)

        # Construct the API request for the current batch
        headers = {'Content-type': 'application/json'}
        data = {
            "seriesid": [series_id],
            "startyear": str(batch_start),
            "endyear": str(batch_end),
            "registrationkey": api_key
        }

        response = requests.post(api_url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            data = json.loads(response.text)
            series_data = data['Results']['series'][0]['data']
            dates = [entry['year'] + '-' + entry['period'].replace("M", "") for entry in series_data]
            unemployment_rates = [float(entry['value']) for entry in series_data]

            # Create a Pandas DataFrame for the current batch
            batch_df = pd.DataFrame({'UnemploymentRate': unemployment_rates}, index=pd.to_datetime(dates, format="%Y-%m"))

            # If df is still None, initialize it with the current batch DataFrame
            if df is None:
                df = batch_df
            else:
                # Concatenate the batch DataFrame with the main DataFrame
                df = pd.concat([batch_df, df])
        time.sleep(5)

    # Save the combined DataFrame to a CSV file
    df.to_csv(f"../input_data/unemployment_data/unemployment_rate_{start_year}_to_{end_year}.csv")
    return df

def get_cpi_data(start_year, end_year):
    # Define the BLS API endpoint and series ID for the unemployment rate
    api_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    series_id = "CUUR0000SA0"  # Unemployment Rate: All Industries, Seasonally Adjusted

    # Initialize an empty DataFrame (set to None initially)
    df = None

    # Define the batch size (20 years in this case)
    batch_size = 20

    # Iterate through years in batches
    for batch_start in range(start_year, end_year, batch_size):
        batch_end = min(batch_start + batch_size - 1, end_year)

        # Construct the API request for the current batch
        headers = {'Content-type': 'application/json'}
        data = {
            "seriesid": [series_id],
            "startyear": str(batch_start),
            "endyear": str(batch_end),
            "registrationkey": api_key
        }

        response = requests.post(api_url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            data = json.loads(response.text)
            series_data = data['Results']['series'][0]['data']
            dates = [entry['year'] + '-' + entry['period'].replace("M", "") for entry in series_data]
            cpi_values = [float(entry['value']) for entry in series_data]

            # Create a Pandas DataFrame for the current batch
            batch_df = pd.DataFrame({'CPI': cpi_values}, index=pd.to_datetime(dates, format="%Y-%m"))

            # If df is still None, initialize it with the current batch DataFrame
            if df is None:
                df = batch_df
            else:
                # Concatenate the batch DataFrame with the main DataFrame
                df = pd.concat([batch_df, df])
        time.sleep(5)

    # Save the combined DataFrame to a CSV file
    df.to_csv(f"../input_data/cpi_data_{start_year}_to_{end_year}.csv")
    return df

import requests
import pandas as pd

def get_population_data(city, start_year, end_year):
    # Define the API endpoint, dataset, and parameters
    base_url = 'https://api.census.gov/data'
    dataset = 'your_dataset'  # Replace with the specific dataset of interest
    location = 'place:*'  # Change to the specific geographic area of interest

    # Create a list to store the data for each year
    data_for_years = []

    for year in range(start_year, end_year + 1):
        # Define the parameters, including the year
        params = {
            'get': 'POP,NAME',
            'for': location,
            'key': CENSUS_API_KEY,
            'year': str(year),
        }

        # Construct the API request URL
        api_url = f"{base_url}/{year}/{dataset}"

        # Make the API request
        response = requests.get(api_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            data_for_years.extend(data)

    # Convert the data into a Pandas DataFrame
    df = pd.DataFrame(data_for_years[1:], columns=data_for_years[0])

    # Filter the DataFrame for the specified city
    city_data = df[df['NAME'] == city]

    return city_data[['POP', 'year', 'NAME']]

def get_long_term_treasury_yields(year):
    # Define the URL for the Treasury yields data
    url = f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_long_term_rate&field_tdr_date_value={year}"

    # Use Pandas to scrape the data table from the URL
    dfs = pd.read_html(url)

    # The first table contains the data you need (10-year and longer-term yields)
    long_term_yields_df = dfs[0]
    # Convert the "Date" column to a datetime object
    long_term_yields_df["Date"] = pd.to_datetime(long_term_yields_df["Date"])
    long_term_yields_df[["Date", "LT COMPOSITE (>10 Yrs)", "TREASURY 20-Yr CMT", "Extrapolation Factor"]].to_csv(f"../input_data/longterm_treasury_rates_data_{year}.csv")

    return long_term_yields_df

# # Example usage with specified date range:
# year= 2023
# df = get_long_term_treasury_yields(year)
# print(df)

# Example usage
# city = 'Los Angeles'  # Replace with the specific city of interest
# start_year = 2000
# end_year = 2001
#
# population_data = get_population_data(city, start_year, end_year)
#
# # Display the DataFrame
# print(population_data)
