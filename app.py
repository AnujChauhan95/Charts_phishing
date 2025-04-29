
import streamlit as st
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load trained model and preprocessors (mock for now)
# In production, replace with: pickle.load(open("model.pkl", "rb"))

st.title("Petroleum Revenue Prediction App")

st.header("Enter Feature Values")

# Input fields for each feature
land_class = st.selectbox("Land Class", ["Federal", "Private", "State"])
land_category = st.selectbox("Land Category", ["Onshore", "Offshore","Not Tied to a Lease"])
state = st.selectbox("State", ["Texas", "Alaska", "California"])  # example states
revenue_type = st.selectbox("Royalties", ["Royalty", "Bonus", "Rent","Inspection fees","Civil penalties", "Other revenue"])
lease_type = st.selectbox("Mineral Lease Type", ["Competitive", "Non-Competitive"])
commodity = st.selectbox("Commodity", ["Oil", "Gas", "Coal"])
county = st.selectbox("County", ["County A", "County B", "County C"])  # example counties
product = st.selectbox("Product", ["Crude Oil", "Natural Gas", "NGL"])

# Collect input in a DataFrame
input_data = pd.DataFrame([{
    "Land Class": land_class,
    "Land Category": land_category,
    "State": state,
    "Revenue Type": revenue_type,
    "Mineral Lease Type": lease_type,
    "Commodity": commodity,
    "County": county,
    "Product": product
}])

# Dummy prediction function for demo purposes
def dummy_model_predict(df):
    for col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    
    # Dummy model
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor()
    model.fit(df_scaled, [123456.78])
    return model.predict(df_scaled)[0]

# Predict and display
if st.button("Predict Revenue"):
    prediction = dummy_model_predict(input_data)
    st.success(f"Estimated Revenue: ${prediction:,.2f}")

st.markdown("""
<hr>
<small>Developed with ❤️ using Streamlit</small>
""", unsafe_allow_html=True)
