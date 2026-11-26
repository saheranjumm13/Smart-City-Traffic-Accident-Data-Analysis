USE smart_city_traffic;

DROP TABLE IF EXISTS road_accidents;
CREATE TABLE road_accidents (
    accident_id INT PRIMARY KEY,
    city VARCHAR(50),
    state VARCHAR(50),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    accident_date VARCHAR(20),
    accident_time VARCHAR(10),
    hour INT,
    day_of_week VARCHAR(15),
    is_weekend INT,
    road_type VARCHAR(30),
    lanes INT,
    traffic_signal INT,
    weather VARCHAR(30),
    visibility VARCHAR(20),
    temperature DECIMAL(5,2),
    traffic_density VARCHAR(20),
    cause VARCHAR(50),
    accident_severity VARCHAR(20),
    vehicles_involved INT,
    casualties INT,
    is_peak_hour INT,
    festival VARCHAR(50),
    risk_score DECIMAL(4,2)
);

-- Q1: Location-wise (City & Road Type) summary
SELECT 
    city,
    state,
    road_type,
    COUNT(*) AS total_accidents,
    SUM(casualties) AS total_casualties,
    SUM(CASE WHEN accident_severity = 'fatal' THEN 1 ELSE 0 END) AS fatal_accidents,
    ROUND(AVG(risk_score), 3) AS avg_risk_score
FROM road_accidents
GROUP BY city, state, road_type
ORDER BY total_accidents DESC;

-- Q2: Time-wise (Hourly & Weekend vs Weekday) trend
SELECT 
    hour,
    is_weekend,
    COUNT(*) AS total_accidents,
    SUM(casualties) AS total_casualties
FROM road_accidents
GROUP BY hour, is_weekend
ORDER BY hour, is_weekend;

-- Q3: Accident-prone spatial grids (Hotspots)
SELECT 
    city,
    road_type,
    ROUND(latitude, 2) AS lat_grid,
    ROUND(longitude, 2) AS lon_grid,
    COUNT(*) AS accidents,
    SUM(casualties) AS casualties,
    ROUND(AVG(risk_score), 3) AS avg_risk_score
FROM road_accidents
GROUP BY city, road_type, ROUND(latitude, 2), ROUND(longitude, 2)
HAVING COUNT(*) >= 5
ORDER BY avg_risk_score DESC, casualties DESC
LIMIT 15;

TRUNCATE TABLE road_accidents;

select * from road_accidents;


SELECT COUNT(*) AS total_rows FROM road_accidents;

-- 1. Location-wise (City & Road Type) summary
SELECT 
    city,
    state,
    road_type,
    COUNT(*) AS total_accidents,
    SUM(casualties) AS total_casualties,
    SUM(CASE WHEN accident_severity = 'fatal' THEN 1 ELSE 0 END) AS fatal_accidents,
    ROUND(AVG(risk_score), 3) AS avg_risk_score
FROM road_accidents
GROUP BY city, state, road_type
ORDER BY total_accidents DESC;

-- 2. Time-wise (Hourly & Weekend vs Weekday) trend
SELECT 
    hour,
    is_weekend,
    COUNT(*) AS total_accidents,
    SUM(casualties) AS total_casualties
FROM road_accidents
GROUP BY hour, is_weekend
ORDER BY hour, is_weekend;

-- 3. Accident-prone spatial hotspots
SELECT 
    city,
    road_type,
    ROUND(latitude, 2) AS lat_grid,
    ROUND(longitude, 2) AS lon_grid,
    COUNT(*) AS accidents,
    SUM(casualties) AS casualties,
    ROUND(AVG(risk_score), 3) AS avg_risk_score
FROM road_accidents
GROUP BY city, road_type, ROUND(latitude, 2), ROUND(longitude, 2)
HAVING COUNT(*) >= 5
ORDER BY avg_risk_score DESC, casualties DESC
LIMIT 15;