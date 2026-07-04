-- How each market's price moved from its first snapshot to its latest
SELECT
    id,
    question,
    FIRST(yes_price ORDER BY captured_at) AS first_price,
    LAST(yes_price ORDER BY captured_at) AS latest_price,
    LAST(yes_price ORDER BY captured_at) - FIRST(yes_price ORDER BY captured_at) AS price_change,
    COUNT(*) AS num_snapshots
FROM market_snapshots
GROUP BY id, question
ORDER BY ABS(price_change) DESC