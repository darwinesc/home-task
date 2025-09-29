import pandas as pd    

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
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
