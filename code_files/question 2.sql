SELECT winner as country,
COUNT(*) AS shootout_wins 
FROM shootouts
GROUP BY winner
ORDER BY country;
