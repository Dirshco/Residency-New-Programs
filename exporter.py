"""
exporter.py

Exports SQLite residency database into:

- CSV
- Excel
- JSON
"""


import os
import pandas as pd
from sqlalchemy import create_engine



DATABASE = (
    "database/residency.db"
)


OUTPUT_FOLDER = "output"



os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)



def load_database():


    engine = create_engine(
        f"sqlite:///{DATABASE}"
    )


    query = """

    SELECT *

    FROM programs

    ORDER BY
    specialty,
    state,
    program_name

    """

    df = pd.read_sql(
        query,
        engine
    )


    return df




def export_csv(df):


    path = os.path.join(
        OUTPUT_FOLDER,
        "residency_new_programs.csv"
    )


    df.to_csv(
        path,
        index=False
    )


    print(
        "CSV created:",
        path
    )





def export_excel(df):


    path = os.path.join(
        OUTPUT_FOLDER,
        "residency_new_programs.xlsx"
    )


    df.to_excel(
        path,
        index=False
    )


    print(
        "Excel created:",
        path
    )





def export_json(df):


    path = os.path.join(
        OUTPUT_FOLDER,
        "residency_new_programs.json"
    )


    df.to_json(
        path,
        orient="records",
        indent=4
    )


    print(
        "JSON created:",
        path
    )


def export_website_json(df):

    import os

    os.makedirs(
        "data",
        exist_ok=True
    )

    path = os.path.join(
        "data",
        "programs.json"
    )

    df.to_json(
        path,
        orient="records",
        indent=4,
        date_format="iso"
    )

    print(
        "Website JSON created:",
        path
    )


def export_all():

    df = load_database()

    export_csv(df)

    export_excel(df)

    export_json(df)

    export_website_json(df)

    return df




if __name__ == "__main__":

    export_all()