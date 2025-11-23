# ETL
import pandas as pd 
import os 

# Extract 
def get_data(input_file="etl_code/hemnet_data_clean.csv"):
    os.makedirs('etl_code/data_ml', exist_ok=True)
    df = pd.read_csv("etl_code/hemnet_data_clean.csv")
    return df #Loading raw data from csv file
    
# Transform 
def transform_data(df):
    try:            
        df = df.dropna(subset=['final_price', 'commune']) # Removing rows with missing columns
        df['sale_date'] = pd.to_datetime(df['sale_date'], format="%Y-%m-%d" ,errors='coerce') # Transforming column date to datetime
        df['month'] = df['sale_date'].dt.month
        df['year'] = df['sale_date'].dt.year
        df = df.drop(columns=df.select_dtypes(include=['bool']).columns)
        df = df.drop(columns=[
            'Unnamed: 0',
            'address', 
            'coordinate', 
            'sale_date',
            'month',
            'year',
            'commune' 
        ]) # Removing irrelevant columns 
        return df
    except Exception as e:
        print(f"An error ocurred: {e}")
        
        
# Load 
def load_csv(df, output_file):
    df.to_csv(output_file, index=False) # Cleaned data
    print(f"Cleaned data saved to {output_file}")
    
    
def main():
    input_file = "etl_code/hemnet_data_clean.csv"
    output_file = "etl_code/data_ml/house_price.csv"
    data = get_data(input_file)
    data = transform_data(data)
    load_csv(data, output_file)
    print("Process completed!")
    
if __name__ == '__main__':
    main()    
        
            
        
         
    
    
