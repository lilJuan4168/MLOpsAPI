
import pandas as pd
import numpy as np
import psycopg2

#connect to database
conn = psycopg2.connect(dbname="streaming", user="root", password="1234", host="localhost", port=5432)
cur = conn.cursor()


#upload amazon dataset
amazon = pd.read_parquet('datasets/amazon.parquet')
amazon = amazon.values.tolist()
cur.executemany(f"INSERT INTO movies_and_series VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", amazon)
conn.commit()
del amazon

#upload disney dataset
disney = pd.read_parquet('datasets/disney.parquet')
disney = disney.values.tolist()
cur.executemany(f"INSERT INTO movies_and_series VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", disney)
conn.commit()
del disney

#upload hulu dataset
hulu = pd.read_parquet('datasets/hulu.parquet')
hulu = hulu.values.tolist()
cur.executemany(f"INSERT INTO movies_and_series VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", hulu)
conn.commit()
del hulu

#upload netflix dataset
netflix = pd.read_parquet('datasets/netflix.parquet')
netflix = netflix.values.tolist()
cur.executemany(f"INSERT INTO movies_and_series VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", netflix)
conn.commit()
del netflix

#upload categories dataset
categories = pd.read_parquet('datasets/categories.parquet')
categories = categories.values.tolist()
cur.executemany(f"INSERT INTO categories VALUES(%s, %s)", categories)
conn.commit()
del categories

#upload platforms_categories dataset
platforms_categories = pd.read_parquet('datasets/platforms_categories.parquet')
platforms_categories = platforms_categories.values.tolist()
cur.executemany(f"INSERT INTO movies_categories VALUES(%s, %s, %s)", platforms_categories)
conn.commit()
del platforms_categories

#upload ratings dataset
ratings = pd.read_parquet('datasets/ratings/ratings_unified1.parquet')
ratings = ratings.values.tolist()
cur.executemany(f"INSERT INTO ratings VALUES(%s, %s, %s, %s)", ratings)
conn.commit()
del ratings
ratings = pd.read_parquet('datasets/ratings/ratings_unified2.parquet')
ratings = ratings.values.tolist()
cur.executemany(f"INSERT INTO ratings VALUES(%s, %s, %s, %s)", ratings)
conn.commit()
del ratings

