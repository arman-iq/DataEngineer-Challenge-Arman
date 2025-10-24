SELECT AVG (home_score + away_score) AS Avg_Goals_Per_Game
FROM results
WHERE date BETWEEN '1900-01-01' AND '2000-12-31';