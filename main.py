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
async def hello():
      return 'WELCOME'
               


#Function 1: return max duration movie name given YEAR, PLATFORM AND DURATION --> str
@app.get('/get_max_duration/{year}/{platform}/{duration_type}') 
async def get_max_duration(year:int, platform:str, duration_type:str = 'min'):
          cur.execute(f'''SELECT title FROM {platform} 
                          WHERE release_year = {year} and type_ = 'movie' and duration_type = duration_type
                          ORDER BY duration_int desc limit 1;''')
          x = cur.fetchall()
          return str(x[0][0])


#Function 2 return the amount of movies given PLATFORM, higher than SCORE and YEAR --> int
@app.get('/get_score_count/{platform}/{scored}/{year}') 
async def get_scored_count(platform:str, scored:float, year:int):
          ratingsfile = pd.read_parquet('datasets/ratings_unified.parquet')
          a = ratingsfile['timestamp']==year
          r = ratingsfile['rating']>scored
          x = ratingsfile[ratingsfile.movieId.str.startswith(pat=list(platform)[0],na=False)][(a) & (r)].shape
          return int(x[0])


#Function 3 return the amount of movies in a given PLATFORM --> int 
@app.get('/get_count_platform/{platform}') 
async def get_count_platform(platform:str):
          cur.execute(f'''SELECT COUNT(title) 
                          FROM {platform} WHERE type_ = 'movie';''' )
          x = cur.fetchall()
          return int(x[0][0])


#Function 4 return the most repeated actor given a PLATFORM and YEAR --> str
@app.get('/get_actor/{platform}/{year}') 
async def get_actor(platform:str, year:int):
          cur.execute(f'''SELECT cast_ FROM {platform} 
                          WHERE release_year = {year}''')
          x = cur.fetchall()
          dt = pd.DataFrame(data=x, columns=['actors'])
          dt = dt['actors'].str.split(pat=',', expand=True)
          dt = dt.to_numpy().reshape(-1,1)
          data = pd.DataFrame(data=dt, columns=['actors'])
          data = data.dropna()
          z = str(data['actors'].value_counts().head(1))
          z = z.split(sep='\n')
          z = z[1].split(sep=' ')
          return z[0]


#Function 5 return the amount of movies given TIPO, PAIS, ANIO --> dic, keys(pais,anio,pelicula)
@app.get('/prod_per_county/{tipo}/{pais}/{anio}') 
async def prod_per_county(tipo:str, pais:str, anio:int):
          cur.execute(f'''SELECT COUNT(title) as peliculas 
                          FROM amazon 
                          WHERE type_ = '{tipo}' and country like '%{pais}%' and release_year = {anio}
                          ;''')
          x = cur.fetchall()
          return {'pais': pais, 'anio': anio, 'pelicula':x[0][0]}


#Function 6 return amount of all movies in steaming given a RATING --> int
@app.get('/get_contents/{rating}') 
async def get_contents(rating):
          cur.execute(f'''SELECT COUNT(title) FROM amazon
                          WHERE rating = '{rating}';''')
          x = cur.fetchall()
          cur.execute(f'''SELECT COUNT(title) FROM disney
                          WHERE rating = '{rating}';''')
          y = cur.fetchall()
          cur.execute(f'''SELECT COUNT(title) FROM hulu
                          WHERE rating = '{rating}';''')
          z = cur.fetchall()
          cur.execute(f'''SELECT COUNT(title) FROM netflix
                          WHERE rating = '{rating}';''')
          k = cur.fetchall()

          return int(x[0][0]+y[0][0]+z[0][0]+k[0][0])


#Function 7 return 5 title base on titulo --> list
@app.get('/get_recommendation/{titulo}')
async def get_recommendation(titulo:str):
        dtml = pd.read_parquet('datasets/streamML.parquet')
        with open('KMeansModel.pickle', 'rb') as model:
                kmeans_model = pickle.load(model)  #ML MODEL
        topredict = dtml[dtml['title'] == titulo][['score','type']].values[0]
        predicted = kmeans_model.predict([topredict])
        x =  dtml[dtml['labels'] == predicted[0]]['title'].head(5)
        return list(x)

