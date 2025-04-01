USE messi_career_data;

SELECT * FROM messi_career_data;

-- Total de goles
SELECT SUM(Goals) AS total_goals FROM messi_career_data;

-- Total de asistencias
SELECT SUM(Assists) AS total_assists FROM messi_career_data;

-- Partidos jugados
SELECT COUNT(*) AS matches_played FROM messi_career_data;

-- Media de minutos por partido
SELECT AVG(Minutes) AS avg_minutes FROM messi_career_data;

SELECT YEAR(Date) AS Year, SUM(Goals) AS Total_Goals
FROM messi_career_data
GROUP BY YEAR(Date)
ORDER BY Year;

SELECT YEAR(Date) AS Year, SUM(Assists) AS Total_Assists
FROM messi_career_data
GROUP BY YEAR(Date)
ORDER BY Year;

SELECT Competition, SUM(Goals) AS Total_Goals
FROM messi_career_data
GROUP BY Competition
ORDER BY Total_Goals DESC
LIMIT 5;

SELECT Date, Competition, `Home Team`, `Away Team`, Goals, Assists,
       (Goals + Assists) AS Goal_Contributions
FROM messi_career_data
ORDER BY Goal_Contributions DESC
LIMIT 10;

