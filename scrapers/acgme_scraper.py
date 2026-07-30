"""
acgme_scraper.py

Purpose:
Import newly accredited residency programs.

Target:
- Internal Medicine
- Family Medicine
- Pediatrics

Years:
- 2025
- 2026

The scraper supports:
1. Manual CSV input
2. Future ACGME webpage/API integration

Output:
Pandas DataFrame
"""


import os
import pandas as pd
from datetime import datetime



ALLOWED_SPECIALTIES = [
    "Internal Medicine",
    "Family Medicine",
    "Pediatrics"
]


ALLOWED_YEARS = [
    2025,
    2026
]


DATA_FILE = os.path.join(
    "data",
    "manual_programs.csv"
)



def clean_columns(df):

    """
    Standardize column names.
    """

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



def load_manual_data():

    """
    Load manually curated ACGME list.

    Example:

    data/manual_programs.csv

    """


    if not os.path.exists(DATA_FILE):

        print(
            "No manual ACGME file found."
        )

        return pd.DataFrame()



    df = pd.read_csv(
        DATA_FILE
    )


    return df



def filter_programs(df):

    """
    Keep only target specialties
    and accreditation years.
    """


    if df.empty:

        return df



    df = clean_columns(
        df
    )



    if "specialty" in df.columns:

        df = df[
            df["specialty"]
            .isin(
                ALLOWED_SPECIALTIES
            )
        ]



    if "accreditation_year" in df.columns:

        df[
            "accreditation_year"
        ] = pd.to_numeric(
            df[
                "accreditation_year"
            ],
            errors="coerce"
        )


        df = df[
            df[
                "accreditation_year"
            ].isin(
                ALLOWED_YEARS
            )
        ]



    return df



def get_new_programs():

    """
    Main function called by pipeline.
    """


    print(
        "Loading ACGME programs..."
    )


    df = load_manual_data()


    df = filter_programs(
        df
    )


    if not df.empty:

        df[
            "last_updated"
        ] = datetime.utcnow()



    print(
        f"Found {len(df)} programs"
    )


    return df



if __name__ == "__main__":

    programs = get_new_programs()

    print(
        programs.head()
    )