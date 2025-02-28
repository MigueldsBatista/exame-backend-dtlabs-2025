-- Filtro dia com servidor, intervalo de tempo e sensor.

SELECT DATE(timestamp_ms) AS day, AVG(humidity) AS avg_humidity
FROM reading
WHERE server_ulid = 'server123'  -- Filtro por servidor
  AND timestamp_ms BETWEEN '2025-02-28 00:00:00' AND '2025-02-28 23:59:59'  -- Filtro de intervalo de tempo
  AND humidity IS NOT NULL  -- Filtrando apenas dados de humidade
GROUP BY day
ORDER BY day;

SELECT DATE(timestamp_ms) AS day, HOUR(timestamp_ms) AS hour, AVG(humidity) AS avg_humidity
FROM reading
WHERE server_ulid = 'server123'
  AND timestamp_ms BETWEEN '2025-02-28 00:00:00' AND '2025-02-28 23:59:59'
  AND humidity IS NOT NULL
GROUP BY day, hour
ORDER BY day, hour;


SELECT DATE(timestamp_ms) AS day, HOUR(timestamp_ms) AS hour, MINUTE(timestamp_ms) AS minute, AVG(humidity) AS avg_humidity
FROM reading
WHERE server_ulid = 'server123'
  AND timestamp_ms BETWEEN '2025-02-28 00:00:00' AND '2025-02-28 23:59:59'
  AND humidity IS NOT NULL
GROUP BY day, hour, minute
ORDER BY day, hour, minute;

-- SEM FILTRO DE SERVIDOR
SELECT 
    DATE(timestamp_ms) AS day,
    HOUR(timestamp_ms) AS hour,
    AVG(temperature) AS avg_temperature
FROM reading
WHERE timestamp_ms BETWEEN '2025-02-28 00:00:00' AND '2025-02-28 23:59:59'
  AND temperature IS NOT NULL
GROUP BY day, hour
ORDER BY day, hour;

-- SEM FILTRO DE INTERVALO DE TEMPO

SELECT 
    DATE(timestamp_ms) AS day,
    HOUR(timestamp_ms) AS hour,
    AVG(humidity) AS avg_humidity
FROM reading
WHERE server_ulid = 'server123'
  AND humidity IS NOT NULL
GROUP BY day, hour
ORDER BY day, hour;


SELECT
    DATE(timestamp_ms) AS day,
    HOUR(timestamp_ms) AS hour,
    AVG(humidity) AS avg_humidity,
    AVG(temperature) AS avg_temperature
FROM reading
WHERE server_ulid = 'server123'
  AND timestamp_ms BETWEEN '2025-02-28 00:00:00' AND '2025-02-28 23:59:59'
  AND (humidity IS NOT NULL OR temperature IS NOT NULL)  -- Considera ambos os tipos de sensor
GROUP BY day, hour
ORDER BY day, hour;