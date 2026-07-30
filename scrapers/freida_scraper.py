"""
freida_scraper.py

Purpose:
Enrich newly accredited residency programs
with IMG-relevant information.

Data fields:
- J1 sponsorship
- H1B sponsorship
- Program type
- Hospital beds
- Website
- Coordinator
- Program Director

Input:
data/freida_programs.csv

Output:
Pandas DataFrame
"""


import os
import pandas as pd



FREIDA_FILE = os.path.join(
    "data",
    "freida_programs.csv"
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



def load_freida_data():

    """
    Load FREIDA enrichment file.

    Example columns:

    program_name
    specialty
    state
    j1_sponsorship
    h1b_sponsorship
    hospital_beds
    program_type

    """


    if not os.path.exists(
        FREIDA_FILE
    ):

        print(
            "No FREIDA data found."
        )

        return pd.DataFrame()



    df = pd.read_csv(
        FREIDA_FILE
    )


    df = normalize_columns(
        df
    )


    return df



def clean_freida(df):


    if df.empty:

        return df



    allowed = [

        "Internal Medicine",
        "Family Medicine",
        "Pediatrics"

    ]


    if "specialty" in df.columns:


        df = df[
            df["specialty"]
            .isin(
                allowed
            )
        ]



    return df



def get_freida_data():


    print(
        "Loading FREIDA enrichment..."
    )


    df = load_freida_data()


    df = clean_freida(
        df
    )


    print(
        f"FREIDA records: {len(df)}"
    )


    return df





def merge_freida(
        acgme_df,
        freida_df
):

    """
    Merge FREIDA information
    into ACGME dataset.
    """


    if freida_df.empty:

        return acgme_df



    merged = acgme_df.merge(

        freida_df,

        on=[
            "program_name",
            "specialty",
            "state"
        ],

        how="left"

    )


    return merged





if __name__ == "__main__":


    data = get_freida_data()

    print(
        data.head()
    )