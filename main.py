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
@app.get('/get_max_duration/{year}/{platform}/{duration_type}') 
def get_max_duration(year:int, platform:str, duration_type:str):
          cur.execute(f"""SELECT title FROM movies_and_series 
                          WHERE release_year = {year} 
                          AND platform = '{platform}' 
                          AND type = 'movie' 
                          ORDER BY duration_int desc 
                          LIMIT 1;""")
          x = cur.fetchall()
          return str(x[0][0])


#Function 2: return the amount of movies given PLATFORM, higher than SCORE and YEAR --> int
@app.get('/get_score_count/{platform}/{scored}/{year}') 
def get_scored_count(platform:str, scored:float, year:int):
          cur.execute(f"""SELECT COUNT(mv.id) FROM movies_and_series mv, ratings r
                          WHERE mv.release_year = {year}
                          AND mv.platform = '{platform}'
                          AND r.rating = {scored};""")
          x = cur.fetchall()
          return x[0][0]


#Function 3 return the amount of movies in a given PLATFORM --> int 
@app.get('/get_count_platform/{platform}') 
def get_count_platform(platform:str):
          cur.execute(f"""SELECT COUNT(id) 
                          FROM movies_and_series 
                          WHERE type = 'movie' 
                          AND platform = '{platform}';""")
          x = cur.fetchall()
          return int(x[0][0])


#Function 4 return the most repeated actor given a PLATFORM and YEAR --> str
@app.get('/get_actor/{platform}/{year}') 
def get_actor(platform:str, year:int):
          cur.execute(f"""SELECT "cast" FROM movies_and_series 
                          WHERE release_year = {year}
                          AND platform = '{platform}';""")
          dt = cur.fetchall()
          dt = pd.DataFrame(data=dt, columns=['cast'])
          dt = dt['cast'].str.split(',', expand=True)
          dt = dt.stack(dropna=True).to_list()
          dt = pd.Series(dt)
          dt = dt.value_counts().sort_values(ascending=False).to_dict()
          del dt['None']
          x = max(dt, key=dt.get)
          y = max(dt.values())
          return [x, y]


#Function 5 return the amount of movies given TIPO, PAIS, ANIO --> dic, keys(pais,anio,pelicula)
@app.get('/prod_per_county/{tipo}/{pais}/{anio}') 
def prod_per_county(tipo:str, pais:str, anio:int):
          cur.execute(f"""SELECT COUNT(title) 
                          FROM movies_and_series 
                          WHERE type = '{tipo}' and country like '%{pais}%' and release_year = {anio}
                          ;""")
          x = cur.fetchall()
          return {'pais': pais, 'anio': anio, 'contenido':x[0][0]}


#Function 6 return amount of all movies in steaming given a RATING --> int
@app.get('/get_contents/{rating}') 
def get_contents(rating):
          cur.execute(f"""SELECT COUNT(movieId) FROM ratings
                          WHERE rating = {rating};""")
          x = cur.fetchall()
          return x[0][0]


#Function 7 return 5 title base on titulo --> list
@app.get('/get_recommendation/{titulo}')
def get_recommendation(titulo:str):
        dtml = pd.read_parquet('datasets/streamML.parquet')
        with open('KMeansModel.pickle', 'rb') as model:
                kmeans_model = pickle.load(model)  #ML MODEL
        topredict = dtml[dtml['title'] == titulo][['score','type']].values[0]
        predicted = kmeans_model.predict([topredict])
        x =  dtml[dtml['labels'] == predicted[0]]['title'].head(5)
        return list(x)