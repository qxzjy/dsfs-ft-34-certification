import streamlit as st
import pandas as pd
import plotly.express as px
import ast

from utils.common import load_delay, create_plot_from_thresholds

# Load data
df_delay = load_delay()

st.markdown("# 🔬 Thresholds analysis")

st.markdown("""
In this section, we'll try to determine the ideal delay between two rentals.
            
To determine the optimum delay, we test several thresholds from 0 to 180 minutes (3 hours) in 10-minute steps
            
As mentioned above, there are two main factors to consider : business and customer satisfaction. To help us decide, we'll try to answer the following questions :
- How many problematic cases will it solve depending on the chosen threshold and scope?
- How many rentals would be affected by the feature depending on the threshold and scope we choose?
- Which share of our owner’s revenue would potentially be affected by the feature?
""")

st.divider()

thresholds = list(range(0, 180, 10))

st.subheader("Problematic cases ❌")

fig_1 = create_plot_from_thresholds(df_delay,
                                    thresholds,
                                    "overlap",
                                    "Threshold (min)",
                                    "Problematic cases solved",
                                    "Number of problematic cases solved depending the threshold and checkin type",
                                    True,
                                    False)

st.plotly_chart(fig_1, use_container_width=True)


st.markdown("""
Before commenting on the results, it's important to note that this graph concerns only those rentals for which we have information on the previous one (i.e. only 9.3% of all data) and which started late, which represents only 169 cases in total (around 1.03%). We can see that with a threshold of 20 minutes, it would already be possible to resolve half the problematic cases, and more than three-quarters if it were 60 minutes (1 hour). However, we rely on too few data to establish a reliable threshold.

As it seems unreliable to use only rentals for which we have information on the previous rental, we will use all of them for the following analysis, with the bias that we don't know the time delta between two rentals.
""")

fig_2 = create_plot_from_thresholds(df_delay,
                                    thresholds,
                                    "delay_at_checkout_in_minutes",
                                    "Threshold (min)",
                                    "Problematic cases solved",
                                    "Number of problematic cases solved depending the threshold and checkin type",
                                    True,
                                    False)

st.plotly_chart(fig_2, use_container_width=True)

st.markdown("""
Unlike before, we're talking here about all rentals that finished late, without taking into account whether they started late, as we don't have the information. In total, there were 9344 problematics cases, which could be halved with an overall threshold of 50 minutes.

However, although setting up a delay between two rentals solves some cases, it does have an impact on rentals returned early and on time, as owners won't be able to return their car to the rental market immediately afterwards, which can lead to lost sales. In the next section, we'll measure the number of rentals affected by the threshold and, above all, how much revenue this represents for the owners revenues.
""")

st.subheader("Rentals affected 🚘")

fig_3 = create_plot_from_thresholds(df_delay,
                                  thresholds,
                                  "delay_at_checkout_in_minutes",
                                  "Threshold (min)",
                                  "Rentals affected",
                                  "Number of rentals affected depending the threshold and checkin type",
                                  False,
                                  False)

st.plotly_chart(fig_3, use_container_width=True)

st.markdown("""
As mentioned above, setting a delay between two rentals is not trivial, as it affects all rentals below the threshold, especially those that are early or on time. We can see from the graph that with a threshold of just 10 minutes, half of all rentals are already affected. And if we go back to the 50-minute threshold, which would resolve half the problem cases, this would affect 70% of all rentals.

Given the large proportion of rentals affected by the introduction of a threshold, it would be interesting to see what this represents in terms of percentage of revenue for owners.
""")

st.subheader("Owner’s revenue impact 💵")

fig_4 = create_plot_from_thresholds(df_delay,
                                  thresholds,
                                  "delay_at_checkout_in_minutes",
                                  "Threshold (min)",
                                  "Potential loss of rental income (%)",
                                  "Percentage of potential loss of rental income depending the threshold and checkin type",
                                  False,
                                  True)

st.plotly_chart(fig_4, use_container_width=True)


st.markdown("""
First of all, it's important to note that market shares are calculated by checkin type and not for all rentals.
As the distribution of checkin types is very unbalanced, connect rentals would be under-represented, whereas in reality they are less prone to delays, and the introduction of a threshold would therefore be more detrimental to their owners.
We can see from the graph that even with a relatively low threshold, a large proportion of revenues can be affected by the introduction of a delay between two rentals.
Another important detail is that we're talking about potential loss of rental income here, as we don't have information on all previous rentals, so we don't know if there's already a time delta between two rentals (if so, the rental is potentially less impacted by the threshold).
""")

st.subheader("How long should the minimum delay be ? ⌚️")

st.markdown("""
From a purely business point of view, given that there are few delays due to others, having the lowest possible threshold would enable us to resolve a proportion of problem cases, while avoiding too many affected rentals and therefore too much potential loss of revenue for owners. For mobile rentals, a threshold of 20 minutes would resolve over 25% of problem cases, while affecting just over 54% of all rentals of this type. However, it doesn't seem appropriate to deploy this feature on connect rentals, as they are much less likely to be late, and would certainly resolve some problem cases (around 30%), but the number of rentals impacted (and therefore possible loss of revenue for owners) would be too high - almost 70%.

However, if only customer satisfaction is taken into account, the threshold would have to be high enough to resolve a large proportion of problem cases, and thus avoid waiting and customer frustration. To resolve around 50% of problem cases, we'd need a threshold of 1 hour for mobile rentals and 40 minutes for connect rentals. It is possible to go further and avoid 75% of problem cases with a threshold of 2 hours 20 minutes for mobile rentals and 1 hour 30 minutes for connect.

To sum up, a high threshold for all types of rental will result in greater customer satisfaction, but a potentially high loss of rental income for owners. The scope of functionality and the ideal threshold will depend on the desired vision, according to objectives in terms of cases solved and sales.
""")