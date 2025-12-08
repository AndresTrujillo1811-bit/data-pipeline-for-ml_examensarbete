import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import joblib

# Loading data and model
data = pd.read_csv("data/house_price.csv")
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
fig, ax = plt.subplots(figsize=(9,5))
predictions["y_true_m"] = predictions["y_true"] / 1_000_000
predictions["y_pred_m"] = predictions["y_pred"] / 1_000_000
sns.scatterplot(x="y_true_m", y="y_pred_m", data=predictions, ax=ax, size=60, alpha=0.6)

minimum = min(predictions["y_true_m"].min(), predictions["y_pred_m"].min())
maximum = max(predictions["y_true_m"].max(), predictions["y_pred_m"].max())

ax.plot([minimum, maximum], [minimum, maximum], 'r--', linewidth=2)
ax.set_xlabel("Actual price in SEK")
ax.set_ylabel("Predicted price in SEK")
ax.set_title("Predictions")
ax.xaxis.set_major_formatter(lambda x, pos: f"{x:.1f}")
ax.yaxis.set_major_formatter(lambda y, pos: f"{y:.1f}")
st.pyplot(fig)




