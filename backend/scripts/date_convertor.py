import pandas as pd

# Function to convert the date format
def convert_date_format(excel_file, target_fields, output_csv):
    df = pd.read_excel(excel_file)

    
    for target_field in target_fields:
        df[target_field] = pd.to_datetime(df[target_field])
        df[target_field] = df[target_field].apply(lambda x: x.strftime('%Y/%m/%d') if pd.notnull(x) else '')

    df.to_csv(output_csv, index=False)
    print(f"File saved as {output_csv}")

excel_file = './data/Market Row Data.xlsx'
target_fields = ['date']
output_csv = './data/market_row_csv.csv'

convert_date_format(excel_file, target_fields, output_csv)

excel_file = './data/User Rates.xlsx'
target_fields = ['effective_date', 'expiry_date']
output_csv = './data/user_rates_csv.csv'

convert_date_format(excel_file, target_fields, output_csv)