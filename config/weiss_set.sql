INSERT INTO WeissSet (id)
SELECT DISTINCT REPLACE(LEFT(number, 3), '/', '') FROM wsdb_eng;
