-- Filter by day with server, time interval and sensor.

SELECT DATE(timestamp_ms) AS day, AVG(temperature) AS avg_humidity
FROM reading
  WHERE timestamp_ms BETWEEN '2025-04-28 00:00:00' AND '2025-06-28 23:59:59'  -- Time interval filter
GROUP BY day
ORDER BY day;


-- Filter by hour with server, time interval and sensor.
SELECT 
    DATE(timestamp_ms) AS day,
    AVG(temperature) AS avg_humidity
FROM reading
WHERE timestamp_ms BETWEEN '2025-04-28 00:00:00' AND '2025-06-28 23:59:59'  -- Time interval filter
GROUP BY day, EXTRACT(HOUR FROM timestamp_ms)
ORDER BY day, EXTRACT(HOUR FROM timestamp_ms);