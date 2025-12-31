# ETL
import pandas as pd 
import os 
import numpy as np 


# Extract 
def get_data(input_file):
    os.makedirs('etl_code/data_ml', exist_ok=True)
    df = pd.read_csv(input_file)
    return df # Loading raw data from CSV-file
     
     
# Transform 
def transform_data(df):
    df.columns = df.columns.str.lower().str.strip()
    if "sale_date" in df.columns:
        print(df["sale_date"].head(10))
    else:
        print("No sale dates found")
        return df        
              
    df = df.dropna(subset=['final_price','commune']) # Removing rows with missing values
    #df = df.dropna(subset=['commune'])
    
    start = pd.Timestamp(2023, 1, 1)
    end = pd.Timestamp(2025, 12, 31)

    days = np.random.randint(0, (end - start).days, size=len(df))
    df['sale_date'] = df['sale_date'] = start + pd.to_timedelta(days, unit='D')
    df['status'] = np.where(np.random.rand(len(df)) > 0.62, "Available", "Sold") 
    #df['status'] = df['final_price'].apply(lambda x: "Available" if pd.isna(x) else "Sold")
    
    df = df.drop(columns=df.select_dtypes(include=['bool']).columns)
    df = df.drop(columns=[
        'unnamed: 0', 
        'coordinate',
        'asked_price',
        'pourcentage_difference',
        'supplemental_area',
    ]) # Removing unnecesary columns
    return df

            
# Load & save
def load_csv(df, output_file):
    df.to_csv(output_file, index=False) # Cleaned data
    print(f"Cleaned data saved to {output_file}")
    
    
# Run the program    
def main():
    input_file = "etl_code/hemnet_data_clean.csv"
    output_file = "etl_code/data_ml/stockholm_homeprices.csv"
    data = get_data(input_file)
    data = transform_data(data)
    load_csv(data, output_file)
    print("Process completed!")
    
if __name__ == '__main__':
    main()   