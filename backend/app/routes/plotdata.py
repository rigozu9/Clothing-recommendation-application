from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_plot_data():
    return {
        "labels": ["black", "white", "blue", "red"],
        "values": [0.4, 0.3, 0.2, 0.1],
}