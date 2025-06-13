import streamlit as st

st.html("<center><img src='https://lever-client-logos.s3.amazonaws.com/2bd4cdf9-37f2-497f-9096-c2793296a75f-1568844229943.png' height='250'></center>")

st.markdown("""
[Getaround](https://fr.getaround.com/) is the Airbnb for cars. You can rent cars from any person for a few hours to a few days! Founded in 2009, this company has known rapid growth. In 2019, they count over 5 million users and about 20K available cars worldwide.

When renting a car, our users have to complete a checkin flow at the beginning of the rental and a checkout flow at the end of the rental in order to:

Assess the state of the car and notify other parties of pre-existing damages or damages that occurred during the rental.
Compare fuel levels.
Measure how many kilometers were driven.
The checkin and checkout of our rentals can be done with three distinct flows:

- 📱 Mobile rental agreement on native apps: driver and owner meet and both sign the rental agreement on the owner’s smartphone
- 🛜 Connect: the driver doesn’t meet the owner and opens the car with his smartphone
- 📝 Paper contract (negligible)

When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.

In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.
""")

st.divider()

st.markdown("""
In addition, we were asked to work on a price optimizer for ownerss to suggest them an optimal price based on all the characteristics of all the rentals that had already taken place.
""")