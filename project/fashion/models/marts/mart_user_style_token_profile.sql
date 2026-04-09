WITH user_tokens AS (
    SELECT
        uli.user_id,
        t.token
    FROM analytics.user_liked_item uli
    JOIN analytics.int_imat_image_tokens t
        ON t.image_id = uli.image_id
),

parsed_tokens AS (
    SELECT
        user_id,
        token,
        split_part(token, ':', 1) AS token_type,
        split_part(token, ':', 2) AS token_value
    FROM user_tokens
),

token_counts AS (
    SELECT
        user_id,
        token_type,
        token_value,
        COUNT(*) AS token_count
    FROM parsed_tokens
    GROUP BY user_id, token_type, token_value
),

ranked_tokens AS (
    SELECT
        *,
        RANK() OVER (
            PARTITION BY user_id, token_type
            ORDER BY token_count DESC
        ) AS token_rank
    FROM token_counts
)

SELECT
    user_id,
    token_type,
    token_value,
    token_count,
    token_rank
FROM ranked_tokens