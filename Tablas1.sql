----se debe crear una sentencia para eliminar la tabla cada que se cree
DROP TABLE IF exists MoviesFinal;

DROP TABLE IF exists ESPACIOS;
CREATE TABLE ESPACIOS AS
    SELECT movieId, RTRIM(title) as title, genres 
    FROM movies;

-- se debe crear una sub sentencia que nombre el elemento. 
----select,titulo y  año

DROP TABLE IF exists MoviesFinal;
CREATE TABLE MoviesFinal AS
  SELECT movieId, SUBSTR(title, 1, len-7) as title, year, genres
      FROM (
        SELECT  title, LENGTH(title) AS len, movieId, SUBSTR(title, -5, 4) AS year, genres
        FROM ESPACIOS);
        


UPDATE MoviesFinal SET year = NULL WHERE NOT year BETWEEN '1901' AND '2019';


---Transform date in ratings table


DROP TABLE IF exists Calificación;

CREATE TABLE Calificación AS
    SELECT userId, movieId, rating, DATETIME(timestamp, 'unixepoch') AS 'date' 
    FROM ratings;
