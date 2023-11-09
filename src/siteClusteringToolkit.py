import pandas as pd

def export_site_featuers():
    df_population = pd.read_csv('../input_data/population_by_zipcode.csv')
    df_property = pd.read_csv('../input_data/property locations.csv')
    df_household = pd.read_csv('../input_data/hh_stats_by_zipcode.csv')

    result1 = pd.merge(df_property, df_population, on='ZipCode', how='left')
    result2 = pd.merge(result1, df_household, on='ZipCode', how='left')
    print(result2.columns)

    result2.to_csv('../output_data/property_locations_with_features.csv')
    return result2