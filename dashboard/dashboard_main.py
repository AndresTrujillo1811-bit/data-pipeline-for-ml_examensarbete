import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import joblib

# Loading data and model
data = pd.read_csv("data/")


st.set_page_config(page_title="House prices in Stockholm", layout="wide")

