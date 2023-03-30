from mlxtend.preprocessing import TransactionEncoder    
import a_Funciones as funciones
import sqlite3 as sql
import pandas as pd
import plotly.express as px

conn = sql.connect('db_movies') 
cur = conn.cursor()

# Para crear las tablas necesarias
funciones.ejecutar_sql('Tablas1.sql', cur)
cur.execute("select name from sqlite_master where type='table' ")
cur.fetchall()

dfmovies = pd.read_sql("""SELECT * FROM moviesFinal""", conn)

# Se separan los géneros de cada película, los cuales están en un solo registro y separados por "|" 
genres = dfmovies['genres'].str.split('|')
te = TransactionEncoder()
genres = te.fit_transform(genres)
genres = pd.DataFrame(genres, columns = te.columns_)

# Se elimina la columna genres que anteriormente contenía la información del género (o los géneros) asociado(s) a la película.
dfmovies.drop(columns=['genres'], inplace=True)

# Se agrega las nuevas columnas dummies con la información de los géneros de cada película.  
dfmovies1 = pd.concat([dfmovies, genres], axis = 1)

# Se reemplaza el False por 0 y el True por 1. 
dic_genres = {False:0, True:1}
dfmovies1[genres.columns] = dfmovies1[genres.columns].replace(dic_genres)

# En este caso solo se convierte el formato de la fecha. 
ratings = pd.read_sql('SELECT * FROM Calificación', conn)

# Se tranforma el tipo de dato de la fecha para que quede con el formato correcto. 
ratings['date'] = pd.to_datetime(ratings['date'])

# Se deben guardar los datos en formato sql para hacer las posteriores consultas
dfmovies1.to_sql('movies3', conn)
ratings.to_sql('ratings3', conn)

# se utiliza la función para hacer consultas de popularidad
funciones.ejecutar_sql('Analisis_Ranking.sql', cur)

# Cantidad de películas por género
pd.read_sql('SELECT * FROM Ranking', conn)

# Cantidad de estrenos por año
pd.read_sql('SELECT * FROM ESTRENOS_POR_ANO', conn)

# Cantidad de géneros por año
pd.read_sql('SELECT * FROM GeneroAnual order by year DESC', conn).head(20)

df1 = pd.read_sql("""SELECT * FROM Populares""", conn)
# Gráfica más populares
fig = px.bar(df1, x='title', y='promedioCalificacion', color_discrete_sequence=["orange"])
fig.update_layout(font=dict(size=15))
fig.show()

df2 = pd.read_sql("""SELECT * FROM MenosPopulares""", conn)
# Gráfica menos populares
fig = px.bar(df2, x='title', y='promediocalificacion', color_discrete_sequence=["orange"])
fig.update_layout(font=dict(size=15))
fig.show()

df3 = pd.read_sql("""SELECT * FROM UsuariosMas""", conn)
# Gráfica usuarios que más vistas tienen
fig = px.bar(df3, x=df3.index, y='vistas', color_discrete_sequence=["orange"])
fig.update_layout(font=dict(size=10))
fig.show()

df4 = pd.read_sql(""" SELECT * FROM FrecuenciaMes""", conn)
# Gráfica frecuencia vistas por mes
fig = px.bar(df4, x='month', y='vistas', color_discrete_sequence=["orange"])
fig.show()

df5 = pd.read_sql(""" SELECT * FROM calificacionesG """, conn)
# Gráfica cantidad de calificaciones por cada ratings
fig = px.bar(df5, x='rating', y='quantity', color_discrete_sequence=["orange"])
fig.show()

df6 = pd.read_sql(""" SELECT * FROM porHora """, conn)
df6 = df6.stack().drop('hour', level=1).reset_index().rename(columns={'level_0':'hour', 'level_1':'genre', 0:'quantity'})
# Gráfica géneros más vistos por horas
fig = px.line(df6, x='hour', y='quantity', color='genre', color_discrete_sequence=px.colors.sequential.Electric)
fig.update_layout(title='Distribución de generos por hora', xaxis_title='Hora', yaxis_title='Reproducciones')
fig.show()