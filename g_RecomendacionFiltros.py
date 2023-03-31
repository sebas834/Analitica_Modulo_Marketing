import pandas as pd
import sqlite3 as sql
from sklearn import neighbors
from ipywidgets import interact ## para análisis interactivo
import sys
import numpy as np
from surprise import Reader, Dataset
from surprise.model_selection import cross_validate, GridSearchCV
from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline, SVD
from surprise.model_selection import train_test_split
from surprise.prediction_algorithms import SlopeOne

conn = sql.connect('db_movies')
cur=conn.cursor()

ratings = pd.read_sql('select * from ratings', conn)

###### leer datos desde tabla de pandas
reader = Reader(rating_scale=(0.5, 5))

##las columnas deben estar en orden estándar: user item rating
data   = Dataset.load_from_df(ratings[['userId','movieId','rating']], reader)

models=[KNNBasic(),KNNWithMeans(),KNNWithZScore(),KNNBaseline()] 
results = {}

for model in models:
 
    CV_scores = cross_validate(model, data, measures=["MAE","RMSE"], cv=5, n_jobs=-1)  
    result = pd.DataFrame.from_dict(CV_scores).mean(axis=0).\
             rename({'test_mae':'MAE', 'test_rmse': 'RMSE'})
    results[str(model).split("algorithms.")[1].split("object ")[0]] = result

performance_df = pd.DataFrame.from_dict(results).T
performance_df.sort_values(by='RMSE')

param_grid = { 'sim_options' : {'name': ['msd','cosine'], \
                                'min_support': [5], \
                                'user_based': [False, True]}
             }

gridsearchKNNBaseline = GridSearchCV(KNNBaseline, param_grid, measures=['rmse'], \
                                      cv=2, n_jobs=2)
                                    
gridsearchKNNBaseline.fit(data)

gridsearchKNNBaseline.best_params["rmse"]
gridsearchKNNBaseline.best_score["rmse"]

################# Realizar predicciones

trainset = data.build_full_trainset()


sim_options       = {'name':'msd','min_support':5,'user_based':True}
model = KNNBaseline(sim_options=sim_options)
model=model.fit(trainset)


predset = trainset.build_anti_testset() 
predictions = model.test(predset) ### función muy pesada
predictions_df = pd.DataFrame(predictions)
# predictions.shape

def recomendaciones(user_id,n_recomend=10):
    
    predictions_userID = predictions_df[predictions_df['uid'] == user_id].\
                    sort_values(by="est", ascending = False).head(n_recomend)

    recomendados = predictions_userID[['iid','est']]
    recomendados.to_sql('reco',conn,if_exists="replace")
    
    recomendados=pd.read_sql('''select a.*, b.title 
                             from reco a left join movies b
                             on a.iid=b.movieId ''', conn)

    return(recomendados)

np.set_printoptions(threshold=sys.maxsize)
predictions_df['uid'].unique()[:20] 

us1 = recomendaciones(user_id=1, n_recomend=20)