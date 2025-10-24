-- only tournaments with scorer data appear
WITH g AS (
  SELECT
    r.tournament,
    gs.scorer,  -- goals scored
    COUNT(*) AS goals  -- total goals scored by that player
  FROM goalscorers gs
  JOIN results r  
    ON gs.date = r.date
   AND gs.home_team = r.home_team
   AND gs.away_team = r.away_team
  WHERE COALESCE(LOWER(TRIM(CAST(gs.own_goal AS CHAR))), '0') NOT IN ('1','true','t','yes','y')   -- remove any own-goals from scorers as it wouldn't be a "real goal"
    AND gs.scorer IS NOT NULL AND TRIM(gs.scorer) <> ''  -- ignore missing scorer names
  GROUP BY r.tournament, gs.scorer
),
tournament_totals AS (  -- all goals including own-goals this time
  SELECT
    tournament,
    SUM(home_score + away_score) AS total_goals  -- total goals in each tournament
  FROM results
  GROUP BY tournament
),
ranked AS (
  SELECT
    g.*,
    tt.total_goals,  -- join total goals for percentage calc
    DENSE_RANK() OVER (PARTITION BY tournament ORDER BY goals DESC) AS rnk  -- rank scorers
  FROM g
  JOIN tournament_totals tt USING (tournament)
)
-- show top scorers and their % of total goals
SELECT
  tournament,
  scorer       AS top_scorer,
  goals        AS goals_scored,
  total_goals,
  ROUND(100.0 * goals / NULLIF(total_goals, 0), 2) AS percent_of_total  -- % of total
FROM ranked
WHERE rnk = 1
ORDER BY tournament, top_scorer;  -- include top scorer as well, for more than 1 play_
