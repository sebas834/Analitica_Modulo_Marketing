import pandas as pd
import joblib
from ipywidgets import interact

# Se cargan los archivos a usar para las recomendaciones
rank_anio = joblib.load('rank_anio.pkl')
rank_dum2 = joblib.load('rank_dum2.pkl')

# Función para hacer las recomendaciones
def recomendacion(movie = list(rank_anio['title'])):
    ind_movie=rank_anio[rank_anio['title']==movie].index.values.astype(int)[0]   
    similar_movie = rank_dum2.corrwith(rank_dum2.iloc[ind_movie,:],axis=1)
    similar_movie = similar_movie.sort_values(ascending=False)
    top_similar_movies=similar_movie.to_frame(name="correlación").iloc[0:11,]
    top_similar_movies['title']=rank_anio["title"]
    
    return top_similar_movies

print(interact(recomendacion))