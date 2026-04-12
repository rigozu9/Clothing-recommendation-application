from sqlalchemy.orm import Session
from app.models.user_style_token_profile import UserStyleTokenProfile

ALLOWED_TOKEN_TYPES = ("color", "material", "style")

def _to_plot_format(rows):
    return {
        "labels": [row[0] for row in rows],
        "values": [row[1] for row in rows],
    }

def get_user_style_profile_data(db: Session, user_id: int):
    rows = (
        db.query(
            UserStyleTokenProfile.token_type,
            UserStyleTokenProfile.token_value,
            UserStyleTokenProfile.token_count,
        )
        .filter(UserStyleTokenProfile.user_id == user_id)
        .order_by(
            UserStyleTokenProfile.token_type.asc(),
            UserStyleTokenProfile.token_count.desc(),
            UserStyleTokenProfile.token_value.asc(),
        )
        .all()
    )

    grouped = {token_type: [] for token_type in ALLOWED_TOKEN_TYPES}

    for token_type, token_value, token_count in rows:
        if token_type in grouped:
            grouped[token_type].append((token_value, token_count))

    return {
        token_type: _to_plot_format(grouped[token_type])
        for token_type in ALLOWED_TOKEN_TYPES
    }
