use exame_backend;


SELECT 
    s.id,
    CASE 
        WHEN MAX(r.timestamp_ms) < NOW() - INTERVAL 10 SECOND THEN 'offline'
        ELSE 'online'
    END AS status
FROM 
    server s
LEFT JOIN 
    reading r ON s.id = r.server_ulid
GROUP BY 
    s.id;
