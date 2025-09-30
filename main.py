import pandas as pd
import uuid
import re
import json
import argparse
import os
from datetime import datetime


# Validate uuid column
def validateId(x):
    try:
        # Intenta convertir a UUID (versión 4 por defecto, pero puede ser flexible)
        uuid_obj = uuid.UUID(str(x))
        return True
    except (ValueError, TypeError):
        return False
    

# Validate datetime format %Y-%m-%dT%H:%M:%S.%f column
def validateDatetime(valor):
    try:
        datetime.strptime(valor, "%Y-%m-%dT%H:%M:%S.%f")
        return True
    except (ValueError, TypeError):
        return False
    
    
# Validate datetime %Y-%m-%d column
def validateDate(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False
    
# Validate a number value     
def validateNumber(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

# Validate a sku value
def validateSku(value):
    try:
        pattern = r'^[A-Za-z0-9]{3}-\d{8}$' # Regex for sku
        return bool(re.fullmatch(pattern, str(value)))
    except (ValueError, TypeError):
        return False
    
# Validate a Product title value
def validateProductTitle(value):
    try:
        pattern = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$'
        return bool(re.fullmatch(pattern, str(value)))
    except (ValueError, TypeError):
        return False
    
# Validate a currency value
def validateCurrency(value):
    try:
        pattern = r'^[A-Za-z0-9]{3}$' # Regex for sku
        return bool(re.fullmatch(pattern, str(value)))
    except (ValueError, TypeError):
        return False
    
def createJsonFile(json_data):
    try:
        # Save the json data in a file
        json_file = "processing_stats.json"
        with open(f"output/{json_file}", "w", encoding="utf-8") as file:
           json.dump(json_data, file, ensure_ascii=False, indent=4)
        print(f"The json file '{json_file}' has been created")
    except (ValueError, TypeError):
        return False

def main():

    try:

        parser = argparse.ArgumentParser(description="Procesar archivo CSV")
        parser.add_argument("path", help="CSV file path")
        args = parser.parse_args()
        file = args.path
        print(f"Read file from: {file}")
       
        # Read csv file and create dataframe
        df = pd.read_csv(file)

        total_rows = len(df.index)
        print("Total rows: ", total_rows)

        # Remove empty rows
        df_empty_rows = df[(df.isnull() | (df == '')).all(axis=1)]
        total_empty_rows = len(df_empty_rows)
        print("Total empty rows: ", total_empty_rows)

        # Remove duplicate rows
        df_duplicates = df[df.duplicated()]
        total_duplicate_rows = len(df_duplicates)
        print("Total duplicates rows: ", total_duplicate_rows)

        # Create a dataframe with discarted rows
        df_discarted_rows = pd.concat([df_empty_rows, df_duplicates], ignore_index=True)

        # Save the dataframe to csv file
        discarded_path = "output/discarded_rows.csv"

        # Create output folder id doesn't exists
        folder = os.path.dirname(discarded_path)
        os.makedirs(folder, exist_ok=True)

        df_discarted_rows.to_csv(f'{discarded_path}', index=False)
        print(f"The csv file '{discarded_path}' has been created")

        # Validate rows
        df['validate_order_id'] = df['order_id'].apply(validateId)
        df['validate_purchased_at'] = df['purchased_at'].apply(validateDatetime)
        df['validate_purchased_date'] = df['purchased_date'].apply(validateDate)
        df['validate_purchased_month_ended'] = df['purchased_month_ended'].apply(validateDate)
        df['validate_order_item_id'] = df['order_item_id'].apply(validateNumber)
        df['validate_sku'] = df['sku'].apply(validateSku)
        df['validate_product_title'] = df['product_title'].apply(validateProductTitle)
        df['validate_product_name_full'] = df['product_name_full'].apply(validateProductTitle)
        df['validate_currency'] = df['currency'].apply(validateCurrency)
        df['valdate_item_price'] = df['item_price'].apply(validateNumber)
        df['validate_item_tax'] = df['item_tax'].apply(validateNumber)
        df['validate_shipping_price'] = df['shipping_price'].apply(validateNumber)
        df['validate_shipping_tax'] = df['shipping_tax'].apply(validateNumber)
        df['validate_gift_wrap_price'] = df['gift_wrap_price'].apply(validateNumber)
        df['validate_gift_wrap_tax'] = df['gift_wrap_tax'].apply(validateNumber)
        df['validate_item_promo_discount'] = df['item_promo_discount'].apply(validateNumber)
        df['validate_shipment_promo_discount'] = df['shipment_promo_discount'].apply(validateNumber)
        df['validate_ship_service_level'] = df['ship_service_level'].apply(validateProductTitle)

        # Validates the entire row
        df['valid_row'] = (
                                df['validate_order_id'] &
                                df['validate_purchased_at'] &
                                df['validate_purchased_date'] &
                                df['validate_order_item_id'] & 
                                df['validate_sku'] &
                                df['validate_product_title'] &
                                df['validate_product_name_full'] &
                                df['validate_currency'] &
                                df['valdate_item_price'] &
                                df['validate_item_tax'] &
                                df['validate_shipping_price'] &
                                df['validate_shipping_tax'] &
                                df['validate_gift_wrap_price'] &
                                df['validate_gift_wrap_tax'] &
                                df['validate_item_promo_discount'] &
                                df['validate_shipment_promo_discount'] &
                                df['validate_ship_service_level']
                            )
        
        df_usable = df[df['valid_row']].copy()

        # Count the usable rows in dataframe
        total_usable_rows = len(df_usable)
        print("Usable rows: ", total_usable_rows)

        # Create a json structure
        json_data = {
            "total_rows": total_rows,
            "total_empty_rows_removed": total_empty_rows,
            "total_invalid_rows_removed": total_duplicate_rows + total_empty_rows,
            "total_duplicate_rows_removed": total_duplicate_rows,
            "total_usable_rows": total_usable_rows
        }

        json_file_response = createJsonFile(json_data)

        # Convert to date type
        df_usable['purchased_date'] = pd.to_datetime(df_usable['purchased_date'])

        # Convert column to numeric
        df_usable['item_price'] = pd.to_numeric(df_usable['item_price'], errors='coerce')
        df_usable['item_promo_discount'] = pd.to_numeric(df_usable['item_promo_discount'], errors='coerce')

        # Calculate the metrics
        #total_item_promo_discount = df_usable.groupby('purchased_date')['item_promo_discount'].sum()
        total_item_promo_discount = df_usable.groupby('purchased_date').agg(total_item_promo_discount=('item_promo_discount', 'sum'))
        sum_item_price = df_usable.groupby('purchased_date')[['item_price', 'item_promo_discount']].sum()
        sum_item_price['total_item_price'] = sum_item_price['item_price'] - sum_item_price['item_promo_discount']
        
        # Union two dataframes inner by purchased_date 
        df_metrics = pd.merge(total_item_promo_discount, sum_item_price, on='purchased_date', how='inner')
        
        # Format the values for each columns and create a csv file
        metrics_path = "output/monthly_metrics.csv"
        df_metrics = df_metrics[['total_item_promo_discount','total_item_price']]
        df_metrics.to_csv(f'{metrics_path}', index=False)
        
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
