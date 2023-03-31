import pandas as pd
import sqlite3 as sql
from mlxtend.preprocessing import TransactionEncoder
import joblib
from sklearn.preprocessing import MinMaxScaler
import a_Funciones as funciones

conn = sql.connect('db_movies')
cur=conn.cursor()

### para verificar las tablas que hay disponibles
cur.execute("SELECT name FROM sqlite_master where type='table' ")
cur.fetchall()

# Se unen las tablas
n_movies = pd.read_sql("""select m.*, r.rating, r.userId from movies m
                left join ratings r on m.movieId = r.movieId""", conn)

# Se crear una serie con el año y se modifica la columna title
anios = n_movies['title'].str.extract(r'\((\d{4})\)', expand = False)
n_movies['title'] = n_movies['title'].str.extract(r'^(.*?)\s*\(', expand = False)
# Se crean una columna con el año
n_movies.insert(1, 'anio', anios)

# Se dividen los géneros
genres = n_movies['genres'].str.split('|')
te = TransactionEncoder()
genres = te.fit_transform(genres)
genres = pd.DataFrame(genres, columns = te.columns_)

# Se elimina la columnas genres
n_movies.drop('genres', axis = 1, inplace = True)

# Se une el df de los géneros con n_movies
movies_final = pd.concat([n_movies, genres], axis = 1)

# Se lleva a formato sql la tabla movies_final
movies_final.to_sql('movies_final', conn, if_exists = 'replace', index = False)

# Se lee la tabla
movies_final = pd.read_sql('select * from movies_final', conn)

# Se guarda la tabla para ser cargada en archivo recomendaciónID
joblib.dump(movies_final, 'movies_final.pkl')

movies_final2= movies_final.loc[:,~movies_final.columns.isin(['userId','movieId','date'])]
movies_final2.to_sql('movies_final2', conn, if_exists='replace')

rank_anio = pd.read_sql("""select *, avg(rating) as avg_rat
                      from movies_final2
                      group by anio, title 
                      order by anio desc, avg_rat desc""", conn)

rank_anio.drop([9724,9725], axis=0, inplace=True)

# convertir año a tipo entero y escalar el año
rank_anio['anio'] = rank_anio.anio.astype('int')
sc=MinMaxScaler()
rank_anio[["anio_"]] = sc.fit_transform(rank_anio[['anio']])

# borrar el año sin escalar y calificaciones  
rank_dum1 = rank_anio.drop(columns=['anio','rating','avg_rat','index'])

# convertir a dummies el nombre de las peliculas
rank_dum2 = pd.get_dummies(rank_dum1,columns=['title'])

# Se muestran las películas que más calificación obtuvieron, ya que
# una película es calificada si es vista y es vista porque quizás vieron el 
# trailer y gustó y puede ser recomendada.
pd.read_sql("""select title, count(rating) as cantidad_calif from movies_final
            group by title 
            order by cantidad_calif desc
            limit 20""", conn)

# Se observan las películas que por año tuvieron, en promedio, el mejor rating.
pd.read_sql("""select anio, title, avg(rating) as prom_rating from movies_final
            group by anio
            order by prom_rating desc
            limit 20
            """, conn)


# Se guardan para ser usados en Recomendacion_Manual
joblib.dump(rank_dum2, 'rank_dum2.pkl')
joblib.dump(rank_anio, 'rank_anio.pkl')

