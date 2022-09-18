# data-ingestion

# Download the data
```bash
$ wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet
$ mv yellow_tripdata_2021-01.parquet data.parquet
```

# Create Docker image
```bash
docker run -it                                     \
  -p 5432:5432                                     \
  -e POSTGRES_USER=root                            \
  -e POSTGRES_PASSWORD=root                        \
  -e POSTGRES_DB=ny_taxi                           \
  -v ${pwd}/postgres_data:/var/lib/postgresql/data \
  postgres
```

# Read data from file
```py
import pandas as pd

# pd.read_parquet needs engine param 
# so you should install pyarrow on pip.
df = pd.read_parquet("data.parquet", engine="pyarrow")

# pd.read_parquet doesn't have any iterator or chunk params.
# If your data is big -like this situation, you should read
# the data chunk by chunk with pyarrow or another engine library.

import pyarrow.parquet as pq

parquet_file = pq.ParquetFile("data.parquet")
for batch in parquet_file.iter_batches():
  df = batch.to_pandas() # df is only include specific chunk of data, not all of them.
```

## Create schema with pandas
```py
# If you need table schema, pandas provides it.

# name param is table name for your sql table
# co is a sql engine(postgresql, mysql etc.). It created by sqlalchemy

from sqlalchemy import create_engine

# We assume postgres running at 5432 
engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")
                                      |     |                    |
                                      |     |                    |
                      POSTGRES_USER----     |                    |
                                            |                    |
                     POSTGRES_PASSWORD-------                    |
                                                 POSTGRES_DB------
# then we connect
engine.connect()

# This function give to us sql table schema.
# We can copy and paste to psql, the table will be created
schema = pd.io.sql.get_schema(df, name="ny_taxi_data", co=engine)
```

## DataFrame to SQL
```py
# Append only first 100 column.
df.head(100).to_sql(con=engine, name="ny_taxi_data", if_exists="replace")

query = """
  select count(1) from ny_taxi_data;
""""

# It gives us 100
df.read_sql(query, con=engine)
```
