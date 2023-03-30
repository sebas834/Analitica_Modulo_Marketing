---tabla de los estrenos por año

DROP TABLE IF exists ESTRENOS_POR_ANO;

CREATE TABLE ESTRENOS_POR_ANO AS
    SELECT year, count(title) AS numberOfMovies 
    FROM movies3 
    GROUP BY year 
    ORDER BY numberOfMovies DESC;

---los generos a loe que pertenece una pelicula(son las más probables)

DROP TABLE IF exists GenerosMovie;

CREATE TABLE GenerosMovie AS
    SELECT title, (Action + Adventure + Animation + Children + Comedy + Crime + Documentary + 
                    Drama + Fantasy + 'Film-Noir' + Horror + IMAX + Musical + Mystery + 
                    Romance + 'Sci-Fi' + Thriller + War + Western) AS total_genres 
    FROM movies3;


---Dias que mas se ven movies

DROP TABLE IF exists FrecuenciaDia;

CREATE TABLE FrecuenciaDia AS
    SELECT strftime('%d', date) AS dia, COUNT(movieId) AS vistas 
    FROM ratings3 
    GROUP BY dia;
    


---usuarios que mas ven peliculas

DROP TABLE IF exists UsuariosMas;

CREATE TABLE UsuariosMas AS
    SELECT COUNT(movieId) AS vistas, userId FROM ratings3 
    GROUP BY userId 
    ORDER BY vistas DESC;
    
----vistos por año

DROP TABLE IF exists frecuenciaAnual;

CREATE TABLE frecuenciaAnual AS
    SELECT strftime('%Y', date) AS year, COUNT(movieId) AS vistas 
    FROM ratings3 
    GROUP BY year;

---vistas por meses


DROP TABLE IF exists FrecuenciaMes;

CREATE TABLE FrecuenciaMes AS
    SELECT strftime('%m', date) AS month, COUNT(movieId) AS vistas 
    FROM ratings3 
    GROUP BY month;

--- niveldecalificaciones  

DROP TABLE IF exists calificacionesG;

CREATE TABLE calificacionesG AS
    SELECT rating, COUNT(UserId) AS quantity
    FROM ratings3
    GROUP BY rating;


---- más populares
DROP TABLE IF exists Populares;

CREATE TABLE Populares AS
    SELECT d.title, c.promedioCalificacion, c.vistas FROM
    (SELECT a.movieId, a.promedioCalificacion, b.vistas 
    FROM (SELECT movieID, AVG(rating) AS promedioCalificacion  
    FROM ratings3 
    GROUP BY movieID) a
    INNER JOIN (SELECT COUNT(userId) AS vistas, movieId FROM ratings3 GROUP BY movieId ORDER BY vistas) b 
    ON a.movieId = b.movieId WHERE b.vistas > 150 ORDER BY a.promedioCalificacion DESC, b.vistas DESC LIMIT 10) c 
    LEFT JOIN movies3 d
    USING(movieId);


-----Horas que más se ve
DROP TABLE IF exists porHora;

CREATE TABLE porHora AS
    SELECT strftime('%H', date) hour, 
                        SUM(Action) as Action,
                        SUM(Adventure) AS Adventure, 
                        SUM(Animation) AS Animation,
                        SUM(Children) AS Children,
                        SUM(Comedy) AS Comedy,
                        SUM(Crime) AS Crime,
                        SUM(Documentary) AS Documentary,
                        SUM(Drama) AS Drama,
                        SUM(Fantasy) AS Fantasy,
                        SUM("Film-Noir") AS FilmNoir,
                        SUM(Horror) AS Horror,
                        SUM(IMAX) AS IMAX,
                        SUM(Musical) AS Musical,
                        SUM(Mystery) AS Mystery,
                        SUM(Romance) AS Romance,
                        SUM("Sci-Fi") AS SciFi,
                        SUM(Thriller) AS Thriller,
                        SUM(War) AS War,
                        SUM(Western) AS Western
    FROM ratings3
    LEFT OUTER JOIN movies3
    USING(movieId)
    GROUP BY hour; 

---Se validan las menos populares, con películas 
DROP TABLE IF exists MenosPopulares;

CREATE TABLE MenosPopulares AS
    SELECT d.title, c.promediocalificacion, c.vistas FROM
    (SELECT a.movieId, a.promediocalificacion, b.vistas 
    FROM (SELECT movieID, AVG(rating) AS promediocalificacion  
    FROM ratings3 
    GROUP BY movieID) a
    INNER JOIN (SELECT COUNT(userId) AS vistas, movieId FROM ratings3 GROUP BY movieId ORDER BY vistas) b 
    ON a.movieId = b.movieId WHERE b.vistas > 50 ORDER BY a.promediocalificacion ASC, b.vistas DESC LIMIT 10) c 
    LEFT JOIN movies3 d
    USING(movieId);
    

--- generos mas vistos

DROP TABLE IF exists Ranking;

CREATE TABLE Ranking AS
    SELECT 
    SUM(Action) AS Action, 
    SUM(Adventure) AS Adventure, 
    SUM(Animation) AS Animation,
    SUM(Children) AS Children,
    SUM(Comedy) AS Comedy,
    SUM(Crime) AS Crime,
    SUM(Documentary) AS Documentary,
    SUM(Drama) AS Drama,
    SUM(Fantasy) AS Fantasy,
    SUM("Film-Noir") AS FilmNoir,
    SUM(Horror) AS Horror,
    SUM(IMAX) AS IMAX,
    SUM(Musical) AS Musical,
    SUM(Mystery) AS Mystery,
    SUM(Romance) AS Romance,
    SUM("Sci-Fi") AS SciFi,
    SUM(Thriller) AS Thriller,
    SUM(War) AS War,
    SUM(Western) AS Western 
    FROM movies3;
    
    
    DROP TABLE IF exists Ranking1;
    
    CREATE TABLE Ranking1 AS
    SELECT 'Action' AS genre, Action as sum FROM Ranking
    UNION ALL
        SELECT 'Adventure' AS genre, Adventure as sum FROM Ranking
    UNION ALL
        SELECT 'Animation' AS genre, Animation as sum FROM Ranking
    UNION ALL
        SELECT 'Children' AS genre, Children as sum FROM Ranking
    UNION ALL
        SELECT 'Comedy' AS genre, Comedy as sum FROM Ranking
    UNION ALL
        SELECT 'Crime' AS genre, Crime as sum FROM Ranking
    UNION ALL
        SELECT 'Documentary' AS genre, Documentary as sum FROM Ranking
    UNION ALL
        SELECT 'Drama' AS genre, Drama as sum FROM Ranking
    UNION ALL
        SELECT 'Fantasy' AS genre, Fantasy as sum FROM Ranking
    UNION ALL
        SELECT 'FilmNoir' AS genre, FilmNoir as sum FROM Ranking
    UNION ALL
        SELECT 'Horror' AS genre, Horror as sum FROM Ranking
    UNION ALL
        SELECT 'IMAX' AS genre, IMAX as sum FROM Ranking
    UNION ALL
        SELECT 'Musical' AS genre, Musical as sum FROM Ranking
    UNION ALL
        SELECT 'Mystery' AS genre, Mystery as sum FROM Ranking
    UNION ALL
        SELECT 'Romance' AS genre, Romance as sum FROM Ranking
    UNION ALL
        SELECT 'SciFi' AS genre, SciFi as sum FROM Ranking
    UNION ALL
        SELECT 'Thriller' AS genre, Thriller as sum FROM Ranking
    UNION ALL
        SELECT 'War' AS genre, War as sum FROM Ranking
    UNION ALL
        SELECT 'Western' AS genre, Western as sum FROM Ranking;
    

---Genero anual

DROP TABLE IF exists GeneroAnual;

CREATE TABLE GeneroAnual AS
    SELECT 
    year,
    SUM(Action) AS Action, 
    SUM(Adventure) AS Adventure, 
    SUM(Animation) AS Animation,
    SUM(Children) AS Children,
    SUM(Comedy) AS Comedy,
    SUM(Crime) AS Crime,
    SUM(Documentary) AS Documentary,
    SUM(Drama) AS Drama,
    SUM(Fantasy) AS Fantasy,
    SUM("Film-Noir") AS FilmNoir,
    SUM(Horror) AS Horror,
    SUM(IMAX) AS IMAX,
    SUM(Musical) AS Musical,
    SUM(Mystery) AS Mystery,
    SUM(Romance) AS Romance,
    SUM("Sci-Fi") AS SciFi,
    SUM(Thriller) AS Thriller,
    SUM(War) AS War,
    SUM(Western) AS Western 
    FROM movies3
    GROUP BY year;
--Analisis_Ranking.sql
--Mostrando Analisis_Ranking.sql.