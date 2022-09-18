import pandas as pd
import pyarrow.parquet as pq

from sqlalchemy import create_engine

def main():
    #generated_schema = pd.io.sql.get_schema(df, name='ny_taxi_data', con=engine)
    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    engine.connect()
    # parquet_data = pq.ParquetFile('./data.parquet')
    #
    # for index, batch in enumerate(parquet_data.iter_batches()):
    #     print(f"{index}. pass")
    #     df = batch.to_pandas()
    #     df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    #     df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    #
    #     try:
    #         df.to_sql(con=engine, name='ny_taxi_data', if_exists='append')
    #         print("SUCCESS")
    #     except:
    #         print("ERROR")

    query = """
        select count(1) from ny_taxi_data
    """

    pd.read_sql(query, con=engine)
if __name__ == '__main__':
    main()
