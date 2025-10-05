from functools import partial
from typing import Any

import numpy as np
import pandas as pd

# Create a Pandas Series with custom index

# Example 1: String index
print(" Example 1: String index")
cities = pd.Series(
    [24.6, 6.3, 19.8, -5.4, 2.8],
    index=["Miami", "Seattle", "Los Angeles", "Chicago", "New York"],
)

print(cities)
# access by custom index
print(f"\nAcess by custom index: {cities['Chicago']}")

# Example 2 : datetime index
print(" Example 2: datetime index")
dates = pd.date_range("2025-01-01", periods=5)
temperature = pd.Series([24.6, 6.3, 19.8, -5.4, 2.8], index=dates)
print(temperature)
print(f"\nAccess by date: {temperature['2025-01-03']}")

# Create a Pandas Dataframe with Clean Weather data
# Read the CSV file clean_weather_data
print("Reading the clean  weather data CSV file...")
df = pd.read_csv("data/clean_weather_data.csv")

# Inspect tha data frame

# Print the dtypes
print("=" * 50)
print("Data types:")
print(df.dtypes)
# Print the first 5 rows
print("=" * 50)
print("First 5 rows info:")
print(df.head())
# Print the last 4 rows
print("=" * 50)
print("Last 4 rows info:")
print(df.tail(4))
# Print basic dataframe statistics
print("=" * 50)
print("Basic dataframe statistics:")
print(df.describe())

# Perform Row slicing
# Row slicing by row position
print("=" * 50)
print("Row slicing by row position : last 7 rows")
last_seven = df[-7:]
print(last_seven)
# Row slicing by column name
print("=" * 50)
print("Row slicing by column name: humidity_percent")
humidity_percent = df["humidity_percent"]
print(humidity_percent)

# Slice the dataframe by boolean flags by the temperature range
# Print the cities with temperature below 3Celsius
print("=" * 50)
print("Cities with temperature records below 3 Degree Celsius:")
very_cold_days = df[["date", "city", "temperature_c"]][df["temperature_c"] < 3]
print(very_cold_days)
# Print the citites with moderate temperature between 10 and 20 degree Celsius
print("=" * 50)
print("Cities with temperature records between 10 and 20 Degree Celsius:")
moderate_temperature = df[df["temperature_c"].between(10, 20)][
    ["date", "city", "temperature_c"]
]
print(moderate_temperature)

##Data Cleaning
# Create a Pandas Dataframe with Messy Weather data
# Read the CSV file messy_weather_data
print("=" * 50)
print("Processing a messy dataframe:")
print("Reading the messy  weather data CSV file...")
messy_df = pd.read_csv("data/messy_weather_data.csv")

# Print its content and data types
print("=" * 50)
print("print first 5 rows and data types ")
print(messy_df.head())
print(messy_df.dtypes)

# Data Cleaning
# Check for duplicates
print("=" * 50)
print("Checking duplicates:")
print("Duplicate Analysis:")
print(f"Total rows: {len(messy_df)}")
print(f"Unique cities: {messy_df['city'].nunique()}")
print(f"Unique dates: {messy_df['date'].nunique()}")
print(
    f"Duplicate cities and dates: {messy_df.duplicated(subset=['city', 'date']).sum()}"
)

# Find duplicate rows
duplicates = messy_df[messy_df.duplicated(subset=["city", "date"], keep=False)]
print("\nDuplicate records:")
print(duplicates)

print("=" * 50)
print("Actual data quality issues:")
print("1. Case sensitivity in city names")
print("2. invalid dates")
print("3. Mixed date formats")
print("4. Actual duplicates")
print("5. Missing values")
print("=" * 50)


# Remove the duplicated rows (keep the first occurence)
def remove_duplicated(df: pd.DataFrame) -> pd.DataFrame:
    print("=" * 50)
    print("removing duplicated rows:")
    df = df.drop_duplicates(subset=["date", "city"], keep="first")
    print(f"After deduplication: {len(df)} rows")
    return df


def standardize_city_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize city names to fix case sensitivity and variations"""
    df_clean = df.copy()
    # Fix case sensitivity
    df_clean["city"] = df_clean["city"].str.title()
    # Fix city name variations
    df_clean["city"] = df_clean["city"].replace(
        {"La": "Los Angeles", "L.A": "Los Angeles"}
    )
    print("Standardized city names")
    return df_clean


def standardize_conditions(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize weather condition names"""
    df_clean = df.copy()
    df_clean["condition"] = df_clean["condition"].str.title()
    print("Standardized condition names")
    return df_clean


df_std_ct = standardize_city_names(messy_df)
df_std_cd = standardize_conditions(df_std_ct)
df_dropped_duplicates = remove_duplicated(df_std_cd)
print("=" * 50)
print("Duplicated rows are removed")
print("Dataframe after removing the duplicates")
print(df_dropped_duplicates)
print("=" * 50)


def safe_type_conversion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Safely convert data types with error handling using pipeline pattern
    Returns the transformed DataFrame and prints dtypes & null counts
    """
    # Convert numeric columns
    numeric_cols = [
        "temperature_c",
        "humidity_percent",
        "wind_speed_kmh",
        "pressure_hpa",
    ]

    print("BEFORE TYPE CONVERSION:")
    print("-" * 30)
    print("Data Types:")
    print(df.dtypes)
    print("\nNull Counts:")
    for col in numeric_cols + ["date"]:
        print(f"{col}: {df[col].isnull().sum()}")

    # Perform type conversions
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    print("\nAFTER TYPE CONVERSION:")
    print("-" * 30)
    print("Data Types:")
    print(df.dtypes)
    print("\nNull Counts:")
    for col in numeric_cols + ["date"]:
        print(f"{col}: {df[col].isnull().sum()}")

    return df


print("-" * 50)
print("Safe Type Conversion")
df_safe_typed = safe_type_conversion(df_dropped_duplicates)
print("DataFrame after safe type conversion")
print(df_safe_typed)
print("-" * 50)


def drop_na_dates(df: pd.DataFrame) -> pd.DataFrame:
    before_count = len(df)
    df_clean = df.dropna(subset=["date"])
    after_count = len(df_clean)
    dropped_count = before_count - after_count
    print(f"\nDropped {dropped_count} rows with invalid dates (NaT values)")
    return df_clean


print("-" * 50)
print("Drop dates that are non valid after safe type check! (NaT values)")
print("Drop NaT values")
print("DataFrame after dropping NaT values")
df_dropped_NAT = drop_na_dates(df_safe_typed)
print(df_dropped_NAT)
print("-" * 50)


def validate_ranges(df: pd.DataFrame) -> pd.DataFrame:
    """Validate data ranges and business rules"""
    issues = []
    # temperature validation
    invalid_temperatures = df[(df["temperature_c"] < -60) | (df["temperature_c"] > 50)]
    if not invalid_temperatures.empty:
        issues.append(f"Invalid temperatures: {len(invalid_temperatures)} records")
        print("=" * 50)
        print("Invalid temperature records:")
        print(invalid_temperatures[["date", "city", "temperature"]])
        print("=" * 50)
        df.loc[
            invalid_temperatures.index, "temperature_c"
        ] = np.nan  # Clean by setting to NaN
    # humidity validation
    invalid_humidities = df[
        (df["humidity_percent"] < 0) | (df["humidity_percent"] > 100)
    ]
    if not invalid_humidities.empty:
        issues.append(
            f"Invalid humidity percentages: {len(invalid_humidities)} records"
        )
        print("=" * 50)
        print("Invalid humidity records:")
        print(invalid_humidities[["date", "city", "humidity_percent"]])
        print("=" * 50)
        df.loc[
            invalid_humidities.index, "humidity_percent"
        ] = np.nan  # Clean by setting to NaN
    # Wind speed validation
    invalid_wind_speeds = df[(df["wind_speed_kmh"] < 0) | (df["wind_speed_kmh"] > 200)]
    if not invalid_wind_speeds.empty:
        issues.append(f"Invalid wind speeds: {len(invalid_wind_speeds)} records")
        print("=" * 50)
        print("Invalid wind speeds records:")
        print(invalid_wind_speeds[["date", "city", "wind_speed_kmh"]])
        print("=" * 50)
        df.loc[
            invalid_wind_speeds.index, "wind_speed_kmh"
        ] = np.nan  # Clean by setting to NaN
    # Pressure validation
    invalid_pressures = df[(df["pressure_hpa"] < 870) | (df["pressure_hpa"] > 1085)]
    if not invalid_pressures.empty:
        issues.append(f"Invalid pressures: {len(invalid_pressures)} records")
        print("=" * 50)
        print("Invalid pressures records:")
        print(invalid_pressures[["date", "city", "pressure_hpa"]])
        print("=" * 50)
        df.loc[
            invalid_pressures.index, "pressure_hpa"
        ] = np.nan  # Clean by setting to NaN
    # Date validation (future dates)
    future_dates = df[df["date"] > pd.Timestamp.now()]
    if not future_dates.empty:
        issues.append(f"Future dates: {len(future_dates)} records")
    return df


print("-" * 50)
print("Range validation")
print("Keeping only the data with valid range")
print("DataFrame after range validation")
df_valid_range = validate_ranges(
    df_dropped_NAT
)  # print invalid values(issues) and replace them with NaN
print(df_valid_range)
print("-" * 50)

# Set Nan values to defaults for every column that has Nan values with .apply()


def default_temp(temp: Any) -> float:
    if pd.isna(temp):
        return 15.0  # default seasonal temp
    return float(temp)


def default_humidity(humidity: Any) -> float:
    if pd.isna(humidity):
        return 65.0  # default humidity
    return float(humidity)


def default_winds(winds: Any) -> float:
    if pd.isna(winds):
        return 10  # default windspeed
    return float(winds)


def default_pressure(pressure: Any) -> float:
    if pd.isna(pressure):
        return 1013  # default pressure
    return float(pressure)


print("-" * 70)
print("Fill the NaN values with chosen default values")
df_filled = df_valid_range.copy()
print("=" * 50)
print("\nBefore filling missing values:")
print(f"Missing temperatures: {df_filled['temperature_c'].isna().sum()}")
print(f"Missing humidity: {df_filled['humidity_percent'].isna().sum()}")
print(f"Missing wind speed: {df_filled['wind_speed_kmh'].isna().sum()}")
print(f"Missing pressure: {df_filled['pressure_hpa'].isna().sum()}")
print("=" * 50)

# apply all the default_functions using .apply() for each column seperately
df_filled["temperature_c"] = df_filled["temperature_c"].apply(default_temp)
df_filled["humidity_percent"] = df_filled["humidity_percent"].apply(default_humidity)
df_filled["wind_speed_kmh"] = df_filled["wind_speed_kmh"].apply(default_winds)
df_filled["pressure_hpa"] = df_filled["pressure_hpa"].apply(default_pressure)

# Print the final cleaned dataframe
print("after filling the missing values:")
print("Final cleaned dataframe:")
print(df_filled)
print("=" * 70)

# Modify the default functions so that they return a df,then use them witihin a pipeline


def default_temperature_entire_df(df: pd.DataFrame) -> pd.DataFrame:
    df["temperature_c"] = df["temperature_c"].apply(
        lambda x: 15 if pd.isna(x) else float(x)
    )
    return df


def default_humidity_entire_df(df: pd.DataFrame) -> pd.DataFrame:
    df["humidity_percent"] = df["humidity_percent"].apply(
        lambda x: 65 if pd.isna(x) else float(x)
    )
    return df


def default_winds_entire_df(df: pd.DataFrame) -> pd.DataFrame:
    df["wind_speed_kmh"] = df["wind_speed_kmh"].apply(
        lambda x: 10 if pd.isna(x) else float(x)
    )
    return df


def default_pressure_entire_df(df: pd.DataFrame) -> pd.DataFrame:
    df["pressure_hpa"] = df["pressure_hpa"].apply(
        lambda x: 1013 if pd.isna(x) else float(x)
    )
    return df


# define an additional function that filters the extreme cold temperatures
# The function requires a thresold paramater
# The function will be included in the pipeline
def filter_extreme_temperatures(
    df: pd.DataFrame, low_threshold: float, high_threshold: float
) -> pd.DataFrame:
    df_filtered = df.copy()

    # Count extremes before filtering
    extreme_low = (df_filtered["temperature_c"] < low_threshold).sum()
    extreme_high = (df_filtered["temperature_c"] > high_threshold).sum()
    print("\nExtreme temperature analysis:")
    print(f"Temperatures below {low_threshold}°C: {extreme_low} records")
    print(f"Temperatures above {high_threshold}°C: {extreme_high} records")
    # flag extreme temperatures
    df_filtered["is_temp_extreme"] = (df_filtered["temperature_c"] < low_threshold) | (
        df_filtered["temperature_c"] > high_threshold
    )
    return df_filtered


print("=" * 90)
print("Implementing a complete data cleaning pipeline using .pipe() and partial")

df_cleaned_by_pipeline = (
    messy_df.pipe(standardize_city_names)
    .pipe(standardize_conditions)
    .pipe(remove_duplicated)
    .pipe(safe_type_conversion)
    .pipe(drop_na_dates)
    .pipe(validate_ranges)
    .pipe(default_temperature_entire_df)
    .pipe(partial(filter_extreme_temperatures, low_threshold=-10, high_threshold=25))
    .pipe(default_humidity_entire_df)
    .pipe(default_winds_entire_df)
    .pipe(default_pressure_entire_df)
)
print("-" * 50)
print("Final cleaned dataframe using a data pipeline:")
print(df_cleaned_by_pipeline)
