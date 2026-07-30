"""
update_database.py

Complete ETL pipeline:

ACGME
+
FREIDA
+
ERAS

into SQLite
"""


from database import (
    create_database,
    add_programs
)

from scrapers.acgme_scraper import (
    get_new_programs
)

from scrapers.freida_scraper import (
    get_freida_data,
    merge_freida
)

from scrapers.eras_scraper import (
    get_eras_data,
    merge_eras
)

from exporter import (
    export_all
)

import pandas as pd
from datetime import datetime



def dataframe_to_records(df):


    df = df.where(
        pd.notnull(df),
        None
    )


    records=[]


    for _, row in df.iterrows():


        record=row.to_dict()


        # Remove invalid keys

        record={
            k:v
            for k,v in record.items()
            if k in [
                c.name
                for c in []
            ]
            or True
        }


        records.append(
            record
        )


    return records




def main():


    print(
        "\nUpdating Residency Database\n"
    )


    create_database()


    # ---------------------------
    # 1. ACGME
    # ---------------------------

    print(
        "Loading ACGME..."
    )

    acgme_df=get_new_programs()



    # ---------------------------
    # 2. FREIDA
    # ---------------------------

    print(
        "Loading FREIDA..."
    )


    freida_df=get_freida_data()


    combined_df=merge_freida(
        acgme_df,
        freida_df
    )



    # ---------------------------
    # 3. ERAS
    # ---------------------------

    print(
        "Loading ERAS..."
    )


    eras_df=get_eras_data()


    combined_df=merge_eras(
        combined_df,
        eras_df
    )



    print(
        "Final programs:",
        len(combined_df)
    )



    # ---------------------------
    # 4. Insert SQLite
    # ---------------------------


    programs=dataframe_to_records(
        combined_df
    )


    add_programs(
        programs
    )



    # ---------------------------
    # 5. Export
    # ---------------------------


    export_all()



    print(
        "\nUpdate Complete"
    )




if __name__=="__main__":

    main()