import argparse
import os
from time import time

import pandas as pd
from sqlalchemy import create_engine


def ingest(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    zip_name = "data.gz"
    csv_name = "output.csv"

    os.system(f"wget {url} -O {csv_name}")
    # os.system(f"gunzip -c {zip_name} > {csv_name}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    df_iter = pd.read_csv(
        csv_name,
        iterator=True,
        chunksize=100000,
    )

    df = next(df_iter)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    while True:
        t_start = time()
        try:
            df = next(df_iter)

            df["lpep_dropoff_datetime"] = pd.to_datetime(df["lpep_dropoff_datetime"])
            df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])

            df.to_sql(name=table_name, con=engine, if_exists="append")

            t_end = time()

            print(f"inserted another chunk..., took {round(t_end-t_start, 3)} seconds")
        except StopIteration:
            print("Done")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")
    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database for postgres")
    parser.add_argument(
        "--table_name", help="name of the table data will be written to"
    )
    parser.add_argument("--url", help="url of csv file")

    args = parser.parse_args()
    ingest(args)
