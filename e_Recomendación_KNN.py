from sklearn import neighbors
import joblib
import pandas as pd
from ipywidgets import interact

# Se cargas los archivos necesarios para hacer la predicción
rank_anio = joblib.load('rank_anio.pkl')
rank_dum2 = joblib.load('rank_dum2.pkl')

model = neighbors.NearestNeighbors(n_neighbors=20, metric='cosine')
model.fit(rank_dum2)
dist, idlist = model.kneighbors(rank_dum2)

distancias=pd.DataFrame(dist)
id_list=pd.DataFrame(idlist)

def movieRecommender(movie_name = list(rank_anio['title'].value_counts().index)):
    movie_list_name = []
    movie_id = rank_anio[rank_anio['title'] == movie_name].index
    movie_id = movie_id[0]
    for newid in idlist[movie_id]:
        movie_list_name.append(rank_anio.loc[newid].title)
    return movie_list_name

print(interact(movieRecommender))