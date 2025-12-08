import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import joblib

# Loading data and model
data = pd.read_csv("data/stockholm_house_price.csv")
models = joblib.load("models/stockholm_house_price.pkl")
predictions = pd.read_csv("data/predictions.csv")

# Title
st.set_page_config(page_title="House prices in Stockholm", layout="wide")
st.title("Stockholm House Price Prediction Dashboard")
st.markdown("Predict final price based on property data from Hemnet.")

# Data insight
st.subheader("Example of cleaned data")
st.dataframe(data.head(10))

# Predictions 
st.subheader("Actual vs Predicted price")
fig, ax = plt.subplots(figsize=(10,6))
predictions["y_true_m"] = predictions["y_true"] / 1_000_000
predictions["y_pred_m"] = predictions["y_pred"] / 1_000_000
sns.scatterplot(x="y_true_m", y="y_pred_m", data=predictions, ax=ax, s=60, alpha=0.6)

minimum = min(predictions["y_true_m"].min(), predictions["y_pred_m"].min())
maximum = max(predictions["y_true_m"].max(), predictions["y_pred_m"].max())

ax.plot([minimum, maximum], [minimum, maximum], 'r--', linewidth=2)
ax.set_xlabel("Actual price in MSEK", fontsize=12)
ax.set_ylabel("Predicted price in MSEK", fontsize=12)
ax.set_title("Actual vs Predicted", fontsize=14)
ax.xaxis.set_major_formatter(lambda x, pos: f"{x:.1f}")
ax.yaxis.set_major_formatter(lambda y, pos: f"{y:.1f}")
st.pyplot(fig)


# Make a prediction
st.subheader("Test your own price prediction")
land_area = st.number_input("Land Area (m²)", min_value=0.0, max_value=2000.0, value=500.0) # Land area (m²)
rooms = st.number_input("Rooms", min_value=1, max_value=12, value=4) # Rooms 
price_per_area = st.number_input("Price per m²", min_value=10000.0, max_value=200000.0, value=80000.0) # Price per area 
communes = [col for col in data.columns if col.startswith('commune')] # Communes
selected_commune = st.selectbox("Choose commune", [c.replace('commune', "") for c in communes]) # Select a commune 


