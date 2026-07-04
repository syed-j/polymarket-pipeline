-- The most recent snapshot for each market (dedupes the raw pile)
WITH ranked AS (
    SELECT
        id,
        question,
        yes_price,
        volume,
        captured_at,
        ROW_NUMBER() OVER (
            PARTITION BY id
            ORDER BY captured_at DESC
        ) AS rn
    FROM market_snapshots
)

SELECT
    id,
    question,
    yes_price,
    volume,
    captured_at
FROM ranked
WHERE rn = 1