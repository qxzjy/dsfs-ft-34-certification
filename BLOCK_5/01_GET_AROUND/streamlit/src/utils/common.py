import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np

DATA_DELAY = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx"
DATA_PRICING = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv"

# DELAY
@st.cache_data
def load_delay():
    data = pd.read_excel(DATA_DELAY, sheet_name="rentals_data")
    
    data = remove_outliers_column_based(data, "delay_at_checkout_in_minutes")

    df_delay_previous = data[["rental_id", "delay_at_checkout_in_minutes"]]
    df_delay_previous.columns = ["previous_ended_rental_id", "previous_delay_at_checkout_in_minutes"]
    data = data.merge(df_delay_previous, on="previous_ended_rental_id", how="left")

    data["overlap"] = data["previous_delay_at_checkout_in_minutes"] - data['time_delta_with_previous_rental_in_minutes']
    data["rental_started_with_delay"] = data["overlap"] > 0
    data["delay_at_checkout"] = data["delay_at_checkout_in_minutes"] > 0
    data["delay_checkout_range"] = data["delay_at_checkout_in_minutes"].transform(create_column_delay_checkout_range)

    return data

# PRICING
@st.cache_data
def load_pricing():
    data = pd.read_csv(DATA_PRICING, index_col=0)
    
    data = remove_outliers_column_based(data, "engine_power")
    data = remove_outliers_column_based(data, "mileage")
    data = remove_outliers_column_based(data, "rental_price_per_day")

    return data


# USEFUL FUNCTIONS
def remove_outliers_column_based(df, column, std_ratio=3) :
    mask = (df[column] > df[column].mean() - std_ratio * df[column].std()) & (df[column] < df[column].mean() + std_ratio * df[column].std())

    return df.loc[mask]


def compute_percentage_on_column(column) :

    return [i / column.sum() * 100 for i in column]


def create_column_delay_checkout_range(delay) :
    if delay <= 0:
        interval = "Early"
    elif delay < 30:
        interval = "Late 0' - 30'"
    elif delay < 60:
        interval = "Late 30' - 60'"
    elif delay < 120 :
        interval = "Late 60' - 120'"
    elif delay >= 120 :
        interval = "Late more than 120'"        
    else :
        interval = "NA"

    return interval

def create_plot_from_thresholds(df, thresholds, column, x_label, y_label, title, only_positive_values, compute_percentage):
    fig = go.Figure()

    total_values = np.zeros(len(thresholds))

    for checkin_type in df["checkin_type"].unique():
        values = []
        mask = (df["checkin_type"] == checkin_type)

        for threshold in thresholds:
            
            if only_positive_values :
                mask &= (df[column] >= 0)

            count = (mask & (df[column] <= threshold)).sum()
            
            if compute_percentage :
                count *= 100 / df[mask].shape[0]

            values.append(count)

            # Set first value to 0 since we don't want to include early and on time rentals when there's no threshold (i.e. set to 0)
            values[0] = 0

        total_values += np.array(values)

        fig.add_trace(go.Scatter(x=thresholds, y=values, mode="lines+markers", name=checkin_type))

    if not compute_percentage :
        fig.add_trace(go.Scatter(x=thresholds, y=total_values, mode="lines+markers", name="total"))

    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)

    return fig