/*
the names of all people who starred in a movie in which Kevin Bacon also starred.
*/
SELECT DISTINCT people.name
FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
-- lấy id_movie mà kevin đóng
WHERE movies.id IN (
    SELECT movies.id FROM movies
    JOIN stars ON movies.id = stars.movie_id
    JOIN people ON people.id = stars.person_id
    WHERE people.name = "Kevin Bacon"
)
-- lấy tên diễn viên != kevin cũng đóng movie đó
AND people.name != "Kevin Bacon";