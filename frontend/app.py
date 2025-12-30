import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import joblib

# Loading data and model
data = pd.read_csv("frontend/data/stockholm_homeprices.csv")
models = joblib.load("frontend/models/stockholm_house_price.pkl")
predictions = pd.read_csv("frontend/data/predictions.csv")

# Get required input columns from training
required_columns = models.named_steps["preprocess"].feature_names_in_

# Title
st.set_page_config(page_title="House prices in Stockholm", layout="wide")
st.title("Stockholm House Price Prediction Dashboard")
st.markdown("Predict final price based on property data from Hemnet.")

# Data overview
st.subheader("Overview")
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


# Make your own prediction
st.subheader("Test your own price prediction")
land_area = st.number_input("Land Area (m²)", min_value=0.0, max_value=2000.0, value=500.0) # Land area
rooms = st.number_input("Rooms", min_value=1, max_value=12, value=4) # Rooms
price_per_area = st.number_input("Price per m²", min_value=10000.0, max_value=200000.0, value=80000.0) # Price per area

# List all commune categories from the training data
commune_values = sorted(data["commune"].unique())
selected_commune = st.selectbox("Choose commune", commune_values)


if st.button("Calculate expected price"):
    input_df = pd.DataFrame([{col: None for col in required_columns}])
   

    # Fill numeric fields
    if "land_area" in input_df.columns:
        input_df.loc[0, "land_area"] = land_area

    if "rooms" in input_df.columns:
        input_df.loc[0, "rooms"] = rooms

    if "price_per_area" in input_df.columns:
        input_df.loc[0, "price_per_area"] = price_per_area

    if "asked_price" in input_df.columns:
        input_df.loc[0, "asked_price"] = land_area * price_per_area

    if "area" in input_df.columns:
        input_df.loc[0, "area"] = land_area

    if "supplemental_area" in input_df.columns:
        input_df.loc[0, "supplemental_area"] = 0

    if "pourcentage_difference" in input_df.columns:
        input_df.loc[0, "pourcentage_difference"] = 0

    if "commune" in input_df.columns:
        input_df.loc[0, "commune"] = selected_commune


    # Convert numeric columns to numbers
    num_cols = models.named_steps["preprocess"].transformers_[0][2]
    input_df[num_cols] = input_df[num_cols].apply(pd.to_numeric, errors="coerce")
    input_df = input_df.fillna(0)


    # Predict
    prediction = models.predict(input_df)[0]
    st.success(f"Final Price: {prediction:,.0f} kr")