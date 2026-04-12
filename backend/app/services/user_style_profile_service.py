from sqlalchemy.orm import Session
from app.models.user_style_token_profile import UserStyleTokenProfile

def get_user_style_plot_data(db: Session, user_id: int, token_type: str = "color"):
    rows = (
        db.query(
            UserStyleTokenProfile.token_value,
            UserStyleTokenProfile.token_count,
        )
        .filter(
            UserStyleTokenProfile.user_id == user_id,
            UserStyleTokenProfile.token_type == token_type,
        )
        .order_by(
            UserStyleTokenProfile.token_count.desc(),
            UserStyleTokenProfile.token_value.asc(),
        )
        .all()
    )

    return {
        "labels": [row[0] for row in rows],
        "values": [row[1] for row in rows],
    }
