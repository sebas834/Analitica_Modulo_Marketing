import joblib
import pandas as pd
import sqlite3 as sql
from ipywidgets import interact ## para análisis interactivo
from sklearn import neighbors

conn = sql.connect('db_movies')
cur = conn.cursor()

cur.execute("select name from sqlite_master where type='table' ")
cur.fetchall()

# Se leen las tablas necesarias para modificar y hacer las predicciones
movies = pd.read_sql('select * from movies', conn)
movies_final = joblib.load("movies_final.pkl")

# Se modifica la tabla
movies_final2 = pd.read_sql('select * from movies_final2', conn)
movies_final2 = movies_final.loc[:,~movies_final.columns.isin(['userId','movieId','date'])]
movies_final2.to_sql('movies_final2', conn, if_exists='replace')
movies_final3 = movies_final2.drop_duplicates(subset = ['title']).reset_index(drop = True)

# Se seleccionan los Ids de los usuarios que votaron en una variable
usuarios = pd.read_sql('select distinct (userId) as user_id from ratings', conn)

# Se usa la función para realizar las predicciones de acuerdo al Id del usuario seleccionado
def recomendar(user_id=list(usuarios['user_id'].value_counts().index)):
  ratings = pd.read_sql('select *from ratings where userId=:user ', conn, params = {'user' : user_id})
  movies_r = ratings['movieId'].to_numpy()
  movies_final3[['movieId','title']] = movies[['movieId','title']]
  movies_f = movies_final3[movies_final3['movieId'].isin(movies_r)]
  movies_f = movies_f.drop(columns = ['anio','title','rating','movieId'])
  movies_f["indice"] = 1 
  centroide = movies_f.groupby("indice").mean()

  movies_nf = movies_final3[~movies_final3['movieId'].isin(movies_r)]
  movies_nf = movies_nf.drop(['anio','title','rating','movieId'], axis = 1)
  model=neighbors.NearestNeighbors(n_neighbors=11, metric='cosine')
  model.fit(movies_nf)
  dist, idlist = model.kneighbors(centroide)

  ids=idlist[0]
  recomend_b=movies.loc[ids][['title']]

  return recomend_b

# Se muestran las predicciones por el Id del usuario
print(interact(recomendar))