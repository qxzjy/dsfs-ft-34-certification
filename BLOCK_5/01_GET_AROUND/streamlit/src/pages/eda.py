import streamlit as st
import plotly.express as px

from utils.common import load_delay, compute_percentage_on_column

# Load data
df_delay = load_delay()

st.markdown("# 📈 EDA")

st.markdown("""
In this section, we present an overview of the data available to us for this study.

The dataset consists of 16276 rows after cleaning. Analysis of the data set shows that only 9.3% of rentals have information on the previous rental, which will be notified when taken into account in the results.

Initially composed of 7 fields, 5 more have been added, their description below:
| Field name | Description |
|:-|:-|
| rental_id  | Unique identifier of the rental. |
| car_id | Unique identifier of the car. |
| checkin_type | Flow used for both checkin and checkout. (ie. access and return the car) Mobile = rental agreement signed on the owner's smartphone Connect = car equiped with the Connect technology, opened by the driver with his smartphone. Note: paper contracts were excluded from the data as we have no data on their delay at checkout and it's negligible use case |
| state | State of the rental. Canceled means that the rental did not happen (was canceled by the driver or the owner). |
| delay_at_checkout_in_minutes | Difference in minutes between the rental end time requested by the driver when booking the car and the actual time the driver completed the checkout. Negative values mean that the driver returned the car in advance. |
| previous_ended_rental_id | Id of the previous ended rental of the car (NULL when no previous rental or delay with previous rental higher than 12 hours). |
| time_delta_with_previous_rental_in_minutes | Difference in minutes between this rental planned start time and the previous rental planned end time (when lower than 12 hours, NULL if higher). |
| previous_delay_at_checkout_in_minutes | Difference in minutes between the previous rental end time requested by the driver when booking the car and the initially planned starting time for the current rental. Negative values mean that the driver returned the car in advance. |
| overlap | Overlap time between the delay of first rental and the time delta initially planned (when we got the information). A negative number means that the delay with the first rental was less than time delta planned with the second rental. |
| rental_started_with_delay | Boolean indicating whether the rental started late. |
| delay_at_checkout | Boolean indicating whether the rental ended late. |
| delay_checkout_range | Same field as delay_at_checkout_in_minutes but represented as a delay interval. |
""")

st.divider()

st.subheader("Dataset overview 🔎")

if st.checkbox("View the data used for this analysis"):
    st.write(df_delay.head(5))

col1, col2 = st.columns(2)

with col1:
    fig_1 = px.pie(
        data_frame=df_delay.groupby("checkin_type").size().reset_index(name="count"),
        names="checkin_type",
        values="count",
        title="Percentage of checkin type"
    )

    st.plotly_chart(fig_1, use_container_width=True)

with col2:
    fig_2 = px.pie(
        data_frame=df_delay["delay_at_checkout"].value_counts().reset_index(),
        names="delay_at_checkout",
        values="count",
        labels={
            "count": "Count",
            "delay_at_checkout": "Delay at checkout"
        },
        title="Percentage of delays"
    )

    st.plotly_chart(fig_2, use_container_width=True)


st.markdown("""
From this global view, we can see that the mobile check-in procedure accounts for 80% of all rentals, compared with 20% for connected cars. We also see that over 57% of rentals end late, representing 9344 rentals out of 16276, given the importance of these figures, we're going to take a closer look at these delays.
""")

st.subheader("Late habit ⌚️")

fig_3 = px.histogram(
    data_frame=df_delay,
    x="delay_at_checkout_in_minutes",
    color_discrete_sequence=[px.colors.qualitative.G10[0]],
    title="Delay at checkout distribution"
)

fig_3.update_layout(
    yaxis_title="Total",
    xaxis_title="Delay at checkout"
)

st.plotly_chart(fig_3, use_container_width=True)

st.markdown("""
A closer look reveals that delays are normally distributed. However, it's important to note that outliers more than three standard deviations from the mean have been removed, as some values seemed to indicate delays of up to almost 49 days, which seems highly unlikely.
""")

df_delay_habit = df_delay[(df_delay["delay_checkout_range"]!="NA")].groupby(["delay_checkout_range", "checkin_type"]).size().reset_index(name="count")

nb_element_connect = df_delay_habit[df_delay_habit["checkin_type"]=="connect"]["count"].sum()
nb_element_mobile = df_delay_habit[df_delay_habit["checkin_type"]=="mobile"]["count"].sum()

df_delay_habit["total"] = df_delay_habit["checkin_type"].apply(lambda x : nb_element_connect if x == "connect" else nb_element_mobile)
df_delay_habit["percentage"] = df_delay_habit["count"] * 100 / df_delay_habit["total"]

fig_4 = px.bar(
    data_frame=df_delay_habit,
    x="checkin_type",
    y="percentage",
    color="delay_checkout_range",
    labels={
        "checkin_type": "Checkin type",
        "percentage": "percentage",
        "delay_checkout_range": "Delay range at checkout"
    },
    title="Distribution of delays by range and type of checkin",
    barmode="group"
)

st.plotly_chart(fig_4, use_container_width=True)


st.markdown("""
We already know that more than half of all rentals end late, but this chart takes our analysis a step further. We can see that connected cars tend to be proportionally less late at the checkout, probably thanks to their faster procedure. Also, it's clear that delay at checkout is mainly within the range 0 to 120 minutes (2 hours), with a majority under 30.
""")

df_delay_impact = df_delay[(df_delay["delay_checkout_range"]!="NA") & (~df_delay["previous_ended_rental_id"].isna())]\
    .groupby(["delay_at_checkout", "rental_started_with_delay"]).size().reset_index(name="count")
df_delay_impact["percentage"] = compute_percentage_on_column(df_delay_impact["count"])

fig_5 = px.bar(
    data_frame=df_delay_impact,
    x="delay_at_checkout",
    y="percentage",
    color="rental_started_with_delay",
    labels={
        "rental_started_with_delay": "Rental started with delay",
        "percentage": "Percentage",
        "delay_at_checkout": "Delay at checkout"
    },
    title="Percentage of rentals with late checkout by late start",
    barmode="group"
)

st.plotly_chart(fig_5, use_container_width=True)

st.markdown("""
Surprisingly, it would appear that despite a late checkin, this is not the main reason for late checkouts, as only 7.47% seem to be due to this. But we have to be careful with these figures, as they only concern rentals for which we have information on previous checkouts (i.e. only 9.3% of all data).

In view of our owner's profit, as well as unsatisfied customers who have to wait, it seems necessary to think about setting a delay between two rentals to avoid cancellations that would be due to a delay by the previous tenant and remove our customer's frustration. For this delay to be relevant, we will try several thresholds that will take into account the specificity of checkin.
""")