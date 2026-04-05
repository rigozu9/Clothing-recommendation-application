from sqlalchemy import text
from sqlalchemy.orm import Session


def get_user_style_plot_data(db: Session, user_id: int, token_type: str = "color"):
    query = text("""
        SELECT
            token_value,
            token_count
        FROM analytics.user_style_token_profile
        WHERE user_id = :user_id
          AND token_type = :token_type
        ORDER BY token_rank
        LIMIT 5
    """)

    result = db.execute(query, {
        "user_id": user_id,
        "token_type": token_type
    })

    rows = result.fetchall()

    labels = [row[0] for row in rows]
    values = [row[1] for row in rows]

    return {
        "labels": labels,
        "values": values
    }