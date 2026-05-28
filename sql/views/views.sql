--- creating views for analysis and visualization ---

Create or replace view vw_monthly_trend as

SELECT month_name, count(*) as total_accidents
from traffic_accidents_final
group by month_name
ORDER BY CASE month_name
    WHEN 'January' THEN 1
    WHEN 'February' THEN 2
    WHEN 'March' THEN 3
    WHEN 'April' THEN 4
    WHEN 'May' THEN 5
    WHEN 'June' THEN 6
    WHEN 'July' THEN 7
    WHEN 'August' THEN 8
    WHEN 'September' THEN 9
    WHEN 'October' THEN 10
    WHEN 'November' THEN 11
    WHEN 'December' THEN 12
END; 

Create or replace view vw_seasonal_trend as

select season, count(*) as total_accidents
FROM traffic_accidents_final
GROUP BY season
ORDER BY CASE season
    WHEN 'Winter' THEN 1
    WHEN 'Spring' THEN 2
    WHEN 'Summer' THEN 3
    WHEN 'Fall' THEN 4
END;

Create or replace view vw_cause_severity_analysis as

select AVG(severity_score) as average_severity_score, cause_category
FROM traffic_accidents_final
GROUP BY cause_category; 

Create or replace view vw_total_injury_by_day as

select AVG(severity_score) as average_severity_score, time_of_day, 
COUNT(injuries_total) as total_accidents_with_injuries
FROM traffic_accidents_final
WHERE injuries_total > 0
GROUP BY time_of_day;

Create or replace view vw_damage_level_distribution as

select AVG(severity_score) as average_severity_score, damage_level, 
count(*) as total_accidents
FROM traffic_accidents_final
GROUP BY damage_level;

DROP VIEW IF EXISTS public.vw_multi_single_unit_comparison;

CREATE VIEW public.vw_multi_single_unit_comparison AS
SELECT 
    multi_unit, 
    COUNT(*) AS total_accidents,
    SUM(CASE 
            WHEN injuries_total > 0 THEN 1 
            ELSE 0 
        END) AS total_accident_with_injuries
FROM traffic_accidents_final
GROUP BY multi_unit;