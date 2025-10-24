SELECT 
REPLACE(date, '-', '') || '_' || substr(home_team, 1,3) || '_' || substr(away_team, 1,3) AS match_key, -- XXXXZZYY_AAA_AAA
date,
home_team,
away_team
FROM shootouts;