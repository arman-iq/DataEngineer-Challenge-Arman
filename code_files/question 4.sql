SELECT
r.date,
r.home_team,
r.away_team,
r.home_score || '-' || r.away_score AS score, -- score format, 1-1
s.winner AS shootout_winner
FROM results r
JOIN shootouts s
ON r.date = s.date
AND r.home_team = s.home_team
AND r.away_team = s.away_team
WHERE r.home_score = 1
AND r.away_score = 1
ORDER BY r.date; -- earliest date