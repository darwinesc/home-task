import pandas as pd
import uuid
from datetime import datetime
import re


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
    

def main():

    try:
       
        # Read csv file and create dataframe
        df = pd.read_csv('input/test.csv')

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
        df_discarted_rows.to_csv('output/discarded_rows.csv', index=False)

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
        
        df_usable = df[df['valid_row']]

        # Count the usable rows in dataframe
        total_usable_rows = len(df_usable)
        print("Usable rows: ", total_usable_rows)

        #print(df_usable)
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
