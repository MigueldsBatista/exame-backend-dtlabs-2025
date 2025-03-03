SELECT
    server_ulid,
    server.server_name,
        -- TO_CHAR(MAX(timestamp_ms), 'DD/MM/YYYY') AS last_reading,   
        -- TO_CHAR(NOW(), 'DD/MM/YYYY') as current_date,
        -- MAX(timestamp_ms) - NOW(),
        CASE
        WHEN MAX(timestamp_ms) >= NOW() - INTERVAL '10 second' THEN 'online'
        ELSE 'offline'
    END AS status
FROM
    reading
inner join server on server.id=reading.server_ulid 
-- where reading.server_ulid  = '01JN7VSV4NR40CVK7RXJG0799G' -- comment this line or not to be get all of the server
GROUP BY
    server_ulid, server_name
ORDER BY
    MAX(timestamp_ms) asc;

    