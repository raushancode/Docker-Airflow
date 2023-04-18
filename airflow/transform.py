import pandas as pd
import extract

def Data_Quality(load_df):
    if load_df.empty:
        print("No Songs Extracted")
        return False
    if load_df.isnull().values.any():
        raise Exception("Null Value Found")

def transform_df(load_df):
    # for future use, currently not transforming data
    return load_df
    


if __name__ == "__main__":
    load_df = extract.return_dataframe()
    Data_Quality(load_df)
    
    transformed_df = transform_df(load_df)
    print(transformed_df)

    
