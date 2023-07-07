#Juan M. Araoz
#Chesteraraoz12.0@gmail.com

from fastapi import FastAPI
from sklearn.cluster import KMeans
import psycopg2
import pandas as pd
import json
import pickle

#Loading configuration data
with open('config.json', 'r') as ld:
        conf = json.load(ld)

#Connection to postgresql server
connection = psycopg2.connect(host = conf['host'],
                              dbname = conf['dbName'], 
                              user= conf['userName'], 
                              password = conf['passwd'], 
                              port = conf['portN'])
cur = connection.cursor()


#Create instance of fastapi
app = FastAPI()

#---------------------------------------------------------------------------------------------------------------
@app.get('/')
def hello():
      return 'WELCOME'
               


#Function 1: return max duration movie name given YEAR, PLATFORM AND DURATION --> str
@app.get('/get_max_duration/{year}/{platform}') 
def get_max_duration(year:int, platform:str):
          cur.execute(f"""SELECT title FROM movies_and_series 
                          WHERE release_year = {year} 
                          AND platform = '{platform}' 
                          AND type = 'movie' 
                          ORDER BY duration_int desc 
                          LIMIT 1;""")
          x = cur.fetchall()
          return str(x[0][0])

