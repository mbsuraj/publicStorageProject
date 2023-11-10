# Public Storage Expansion vs Contraction Analysis

## Assignment Objective

The objective of this assignment is to assist Public Storage (PS) in making informed decisions regarding the expansion or contraction of their rental storage facilities. By analyzing various aspects of the PS business, its stores, locations, ratings, macroeconomic factors, and square footage (sqft) covered, we aim to provide insights that will aid in making strategic decisions.

## Project Flow

The assignment consists of the following key components:

1. **eda.ipynb**: This Jupyter Notebook delves into different aspects of PS's business, exploring its stores, their locations, ratings, and the relationship with macroeconomic variables such as square footage covered. It serves as the exploratory data analysis stage of the project.

2. **parametric_forecast_rentable_sqft.ipynb**: In this Notebook, parametric forecasting methods are applied to predict rental storage expansion based on historical data and various parameters.

3. **nonparametric_forecast_rentable_sqft.ipynb**: This Notebook focuses on non-parametric forecasting techniques, offering an alternative approach to predicting rental storage expansion without making strong assumptions about the data.

## How to use:
1. Both **parametric_forecast_rentable_sqft.ipynb** and **nonparametric_forecast_rentable_sqft.ipynb** can be run for different states. You just need to change one variable called **state**. I've tested it with CA, TX, AZ, FL; you can also put United States as state to see recommendations at country level

## Assumptions:
1. Price of the business is assumed to be same at all times
2. The occupancy of all the stores is assumed to be same at 90% at all times.
3. No discounts.
4. The properties shared by PS are all the properties belonging to PS
5. Historical addition of rental square footage was also done based on demand forecasting and hence assumed a reliable feature
6. CompletionDate assumed to be the day of start of the give site.

## Support Code

The project includes a `src` directory with essential support code:

1. **forecastingToolkit.py**: Contains functions used during the forecasting process, helping to streamline the analysis and modeling.

2. **macroEconomicsToolkit.py**: This module facilitates the retrieval of macroeconomic data through API calls. It provides information on factors such as the Consumer Price Index (CPI), Unemployment rate, and the Public Storage America, Inc. (PSA) stock price.

3. **site_clustering.py**: Although incomplete due to time constraints, this script is intended to house all the code necessary for clustering PS sites. Clustering would help identify patterns and insights related to the site locations.

4. **stockPriceToolkit.py**: This toolkit is designed to retrieve stock price information for any stock, providing valuable financial data for analysis.


## Directories

1. **Input_data**: This folder contains several data files. For the assignment, we primarily use the following files to drive the analysis:
   
   - `property_data.csv`: Property data that serves as a key data source for the project.
   - `population_1950_to_2037_projections/united-states-population-2023-11-07.csv`: Population of the US from 1950 to 2023
   - `us_unemployment_rate_1960-2023.csv`: us_unemployment_rate from 1960 to 2023
   - `long-term-rates-1965_to_2023.csv`: LT interest rates pulled in as they also affect mortgage rates
   - `hh_stats_by_zipcode.csv`: household states such as hh size, income etc by zipcode


2. **Output_data**: Intended to store output data generated from the models, this folder currently hosts the `final_property_locations_with_features.csv` file. This dataset was prepared for site clustering, though the clustering analysis is pending completion.

## Next steps I would Have considered:
1. Exploring more models (maybe 1 or 2 more)
2. Stacking the models to make collective predictions for a state
3. Clustering sites in a state and then running the same forecasts for each state X cluster

## Required Libraries

All the necessary Python libraries required for the assignment are listed in the `requirements.txt` file. You can use this file to ensure you have the correct versions of the libraries installed in your Python environment.

By following the outlined project flow and utilizing the provided support code and data, I can aim to assist Public Storage in making data-driven decisions regarding their rental storage facilities.
