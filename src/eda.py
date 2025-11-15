# EDA analysis for solar radiation data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load data 
def load_data(filepath):
    return pd.read_csv(filepath, parse_dates=['Timestamp'])

# Summary Statistics
# Summary Statistics
def summary_statistics(df):
    return df.describe()

# Data Quality Check:
def data_quality_check(df):
    missing_values = df.isnull().sum() 
    negative_values = df[['GHI', 'DNI', 'DHI']][(df['GHI'] < 0) | (df['DNI'] < 0) | (df['DHI'] < 0)] 
    return missing_values, negative_values 


# Time Series Analysis

def time_series_analysis(df):
    plt.figure(figsize=(15, 8))
    plt.plot(df['Timestamp'], df['GHI'], label='GHI')
    plt.plot(df['Timestamp'], df['DNI'], label='DNI')
    plt.plot(df['Timestamp'], df['DHI'], label='DHI')
    plt.plot(df['Timestamp'], df['Tamb'], label='Tamb')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.title('Time Series Analysis')
    plt.show()

#Correlation Analysis
def correlation_analysis(df):
    variables = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'WS', 'WSgust', 'WD']
    df_selected = df[variables]
    correlation_matrix = df_selected.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix: Solar Radiation, Temperature, and Wind Conditions')
    plt.show()
    # Pair plot for all selected variables
    sns.pairplot(df_selected, diag_kind='kde')
    plt.suptitle("Pair Plot: Solar Radiation, Temperature, and Wind Conditions", y=1.02)
    plt.show()
    # Scatter plots: Wind conditions vs Solar Irradiance
    wind_vars = ['WS', 'WSgust', 'WD']
    solar_vars = ['GHI', 'DNI', 'DHI']
    sns.pairplot(df, x_vars=wind_vars, y_vars=solar_vars, kind='scatter')
    plt.suptitle("Scatter Matrices: Wind Conditions vs Solar Irradiance", y=1.02)
    plt.show()
# wind analysis
def wind_analysis(df):
    plt.figure(figsize=(15, 8))
    plt.plot(df['Timestamp'], df['WS'], label='Wind Speed')
    plt.plot(df['Timestamp'], df['WSgust'], label='Wind Gust')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Wind Speed (m/s)')
    plt.title('Wind Speed and Gust over Time')
    plt.show()
def wind_analysis1(df):
     # Convert wind direction from degrees to radians for polar plot
    wind_direction_rad = np.deg2rad(df['WD'])
    wind_speed = df['WS']

    # Create a radial bar plot
    plt.figure(figsize=(10, 8))
    ax = plt.subplot(111, polar=True)
    bars = ax.bar(wind_direction_rad, wind_speed, width=0.1, color='skyblue', edgecolor='black', alpha=0.7)

    # Customize the polar plot
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title("Radial Plot: Wind Speed and Direction", va='bottom')
    plt.show()

# Temperature Analysis 
def temperature_analysis(df):
    # Scatter plots to show RH vs Temperature and Solar Radiation components
    plt.figure(figsize=(15, 8))

    # Subplot for RH vs Temperatures
    plt.subplot(1, 2, 1)
    plt.scatter(df['RH'], df['TModA'], label='Module A Temperature', alpha=0.7, color='blue')
    plt.scatter(df['RH'], df['TModB'], label='Module B Temperature', alpha=0.7, color='green')
    plt.scatter(df['RH'], df['Tamb'], label='Ambient Temperature', alpha=0.7, color='orange')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('Temperature (°C)')
    plt.title('RH vs Temperatures')
    plt.legend()

    # Subplot for RH vs Solar Radiation components
    plt.subplot(1, 2, 2)
    plt.scatter(df['RH'], df['GHI'], label='GHI', alpha=0.7, color='red')
    plt.scatter(df['RH'], df['DNI'], label='DNI', alpha=0.7, color='purple')
    plt.scatter(df['RH'], df['DHI'], label='DHI', alpha=0.7, color='brown')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('Solar Radiation')
    plt.title('RH vs Solar Radiation')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Historgram Analysis
def histograms(df):
    # Histograms for solar radiation variables
    df[['GHI', 'DNI', 'DHI']].hist(bins=20, figsize=(12, 8), color='skyblue', edgecolor='black')
    plt.suptitle('Histograms of Solar Radiation Variables', fontsize=16)
    plt.tight_layout()
    plt.show()

    # Histograms for temperature variables
    df[['Tamb', 'TModA', 'TModB']].hist(bins=20, figsize=(12, 8), color='lightgreen', edgecolor='black')
    plt.suptitle('Histograms of Temperature Variables', fontsize=16)
    plt.tight_layout()
    plt.show()

    # Histogram for wind speed
    df[['WS']].hist(bins=20, figsize=(6, 5), color='orange', edgecolor='black')
    plt.suptitle('Histogram of Wind Speed', fontsize=16)
    plt.tight_layout()
    plt.show()

# z-score analysis
def z_score_analysis(df, columns, threshold=3):
    z_scores = df[columns].apply(lambda x: (x - x.mean()) / x.std())
    flagged_outliers = (z_scores.abs() > threshold).any(axis=1)

    # Add Z-scores and outlier flags to the DataFrame
    for col in columns:
        df[f"{col}_zscore"] = z_scores[col]
    df["Outlier_Flag"] = flagged_outliers

    return df

# Buble chart
def bubble_chart(df, x_col, y_col, size_col, color_col, title):
     plt.figure(figsize=(10, 6))
     scatter = plt.scatter(
        df[x_col], df[y_col],
        s=df[size_col] * 10,  
        c=df[color_col], cmap='viridis', alpha=0.7, edgecolors='k')
     plt.colorbar(scatter, label=color_col)
     plt.xlabel(x_col)
     plt.ylabel(y_col)
     plt.title(title)
     plt.grid(alpha=0.3)
     plt.show()

# data cleaning
def data_cleaning(df):
    # Fill missing values with the median for numerical columns
    df.fillna(df.median(numeric_only=True), inplace=True)
    
    # Remove negative values from solar radiation columns
    df = df[(df['GHI'] >= 0) & (df['DNI'] >= 0) & (df['DHI'] >= 0)]
    
    # Drop irrelevant columns
    if 'Comments' in df.columns:
        df = df.drop(columns=['Comments'])
    
    return df

def detect_outliers(df, column, threshold=3):   
    mean = df[column].mean()
    std_dev = df[column].std()
    z_scores = (df[column] - mean) / std_dev
    outliers = df[np.abs(z_scores) > threshold]
    return outliers
        



