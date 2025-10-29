# ETL
import pandas as pd 


# Extract 
def get_data(filepath):
    df = pd.read_csv(filepath)  #Loading raw data from csv file
    return df
    
# Transform 
def transform_data(df):
    try: 
        df = df.dropna(subset=['final_price', 'commune']) # Removing rows with missing columns
        df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce') # Transforming column date to datetime
        df['month'] = df['sale_date'].dt.month
        df['year'] = df['sale_date'].dt.year
        df = pd.get_dummies(df, columns=['area', 'commune'], drop_first=True) # Area and commune
        
    except Exception as e:
        print(f"An error ocurred: {e}")
        
         
    
    
