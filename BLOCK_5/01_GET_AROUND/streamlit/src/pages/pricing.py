import requests
import streamlit as st

st.markdown("# 💵 Daily rental price prediction")

car_model = ["Alfa Romeo", "Audi", "BMW", "Citroën", "Ferrari", "Fiat",
             "Ford", "Honda", "KIA Motors", "Lamborghini", "Lexus", "Maserati",
             "Mazda", "Mercedes", "Mini", "Mitsubishi", "Nissan", "Opel",
             "Peugeot", "PGO", "Porsche", "Renault", "SEAT", "Subaru",
             "Suzuki", "Toyota", "Volkswagen", "Yamaha"]

car_type = [ "Convertible","Coupe", "Estate", "Hatchback", "Sedan", "Subcompact",
             "SUV", "Van"]

car_color = ["Silver", "Beige", "White", "Blue", "Grey", "Brown", "Black", "Orange",
             "Red", "Green"]

car_fuel = {
    "Diesel": "diesel",
    "Hybrid": "hybrid_petrol",
    "Petrol": "petrol"
}

with st.form("rental_price_predict"):

    col1, col2 = st.columns(2)

    with col1:
        model = st.selectbox("Model", car_model, placeholder="Model")
        
        milage = st.slider("Mileage", min_value=0, max_value=330000, value=140000, step=100)

        paint_color = st.selectbox("Color", car_color, placeholder="Color")

    with col2:
        type = st.selectbox("Type", car_type, placeholder="Type")

        engine_power = st.slider("Engine power", min_value=0, max_value=250, value=120, step=5)

        fuel =  st.radio("Fuel", list(car_fuel.keys()), horizontal=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        private_parking = st.toggle("Private parking")

        gps = st.toggle("GPS")

        winter_tires = st.toggle("Winter tires")

    with col2:
        air_conditioning = st.toggle("Air conditioning")

        automatic = st.toggle("Automatic")
        
    with col3:
        getaround_connect = st.toggle("Getaround Connect")

        speed_regulator = st.toggle("Speed regulator")

    submitted = st.form_submit_button("Estimate")

    if submitted:

        payload = {
            "model_key": model,
            "mileage": milage,
            "engine_power": engine_power,
            "fuel": car_fuel[fuel], 
            "paint_color": paint_color.lower(),
            "car_type": type.lower(),
            "private_parking_available": private_parking,
            "has_gps": gps,
            "has_air_conditioning": air_conditioning,
            "automatic_car": automatic,
            "has_getaround_connect": getaround_connect,
            "has_speed_regulator": speed_regulator,
            "winter_tires": winter_tires
        }

        request = requests.post("https://qxzjy-get-around-fastapi.hf.space/predict", json=payload)
        response = request.json()

        st.write(f"Estimated daily rental price : {round(response['prediction'], 2)} $")