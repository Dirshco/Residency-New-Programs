"""
eras_scraper.py

Purpose:
Add ERAS-related information.

Fields:
- ERAS participation
- First application cycle
- NRMP code
- Program website

Input:
data/eras_programs.csv

Output:
Pandas DataFrame
"""


import os
import pandas as pd



ERAS_FILE = os.path.join(
    "data",
    "eras_programs.csv"
)



def normalize_columns(df):


    df.columns = (

        df.columns
        .str.strip()
        .str.lower()
        .str.replace(
            " ",
            "_"
        )

    )


    return df





def load_eras_data():


    if not os.path.exists(
        ERAS_FILE
    ):

        print(
            "No ERAS file found."
        )

        return pd.DataFrame()



    df = pd.read_csv(
        ERAS_FILE
    )


    return normalize_columns(
        df
    )





def clean_eras(df):


    if df.empty:

        return df



    specialties = [

        "Internal Medicine",
        "Family Medicine",
        "Pediatrics"

    ]


    if "specialty" in df.columns:


        df = df[
            df.specialty.isin(
                specialties
            )
        ]



    return df





def get_eras_data():


    print(
        "Loading ERAS information..."
    )


    df = load_eras_data()


    df = clean_eras(
        df
    )


    print(
        f"ERAS records: {len(df)}"
    )


    return df





def merge_eras(
        main_df,
        eras_df
):


    if eras_df.empty:

        return main_df



    merged = main_df.merge(

        eras_df,

        on=[
            "program_name",
            "specialty",
            "state"
        ],

        how="left"

    )


    return merged





if __name__ == "__main__":


    df = get_eras_data()

    print(
        df.head()
    )